from types import SimpleNamespace
from sanic.log import logger
from sanic_ext import openapi
from sanic_ext import validate
from sanic.response import json
from sanic import Sanic
from typing import Dict
import attrs
import json as js
from datetime import datetime
from pytz import timezone
import time
import socket

from .config import AppConfig
from .schemas.alerts import TradingViewAlert, TradingViewAlertSchema
from .actions.carbon import send_metric


class TvTraderContext(SimpleNamespace):
    _carbon_sock = None

    def __init__(self, **kwargs: any) -> None:
        super().__init__(**kwargs)

    @property
    def carbon_sock(self):
        return self._carbon_sock

    @carbon_sock.setter
    def carbon_sock(self, sock: socket.socket) -> None:
        self._carbon_sock = sock

    @carbon_sock.deleter
    def carbon_sock(self):
        self._carbon_sock.shutdown()
        self._carbon_sock.close()
        del self._carbon_sock


wsclients = set()

carbon_connection = None
try:
    carbon_connection = socket.create_connection(
        (AppConfig.CARBON_HOST, AppConfig.CARBON_PORT))
except ConnectionRefusedError:
    logger.error("[ERROR] Carbon connection is not available.")

appctx = TvTraderContext()
appctx.carbon_sock = carbon_connection
app = Sanic("TvTrader", config=AppConfig(),
            configure_logging=True, ctx=appctx)


@app.get("/")
@openapi.tag("backend")
@openapi.summary("Healthcheck endpoint")
def check(request):
    return json("HEALTHY " + app.config.APPNAME)


@app.post("/alert")
@openapi.tag("frontend")
@openapi.operation("frontendAlert")
@openapi.body({
    "application/json": TradingViewAlertSchema},
    description="Alert from TradingView forwarded to the frontend",
    required=True,
    name="data",
)
@openapi.response(200, "OK", description='Success')
@openapi.response(400, description="Error occurred. See ERROR property in the response")
@validate(json=TradingViewAlert)
async def alert_post(request, body: TradingViewAlert):
    """
    Alert POST endpoint to proxy the alerts to the frontend application.
    """
    try:
        jsondata = attrs.asdict(body)
        add_timezone_info(jsondata)
        format_json_input(jsondata)
    except Exception as ex:
        return json({"ERROR": str(ex)}, status=400)
    await action_ws_send(jsondata)
    return json("OK")


@app.post("/carbon-alert")
@openapi.tag("backend")
@openapi.operation("carbonAlert")
@openapi.body({
    "application/json": TradingViewAlertSchema},
    description="Alert from TradingView forwarded to Carbon",
    required=True,
    name="data"
)
@openapi.response(200, "OK", description='Success')
@openapi.response(400, description="Error occurred. See ERROR property in the response")
@validate(json=TradingViewAlert)
async def carbon_alert_post(request, body: TradingViewAlert):
    """
        Alert POST endpoint to forward the alerts to a Carbon server.
    """
    try:
        jsondata = attrs.asdict(body)
        add_timezone_info(jsondata)
        format_json_input(jsondata)
    except Exception as ex:
        return json({"ERROR": str(ex)}, status=400)
    # Message meaning conversion to numbers
    config = Sanic.get_app().config
    value = config.CARBON_SELL_VALUE if jsondata["direction"] == "SELL" else config.CARBON_BUY_VALUE
    timediff = int(time.time()) - \
        (jsondata["timestamp"] + jsondata["utcoffset"])
    if timediff > (config.GR_TIMEOUT * 60):
        value = int((config.CARBON_SELL_VALUE + config.CARBON_BUY_VALUE) / 2)
    # Message prepare
    msg = f'strat.{jsondata["stratName"]}.{jsondata["interval"]}.{jsondata["symbol"]} {value} {jsondata["timestamp"]}\n'
    await send_metric(msg)
    return json("OK")


@app.websocket("/wsalerts")
async def feed(request, ws):
    """
        Websocket endpoint for the connected clients.
    """
    logger.debug("ws request: " + str(request))
    wsclients.add(ws)
    while True:
        data = None
        data = await ws.recv()
        if data is not None:
            logger.debug("ws data received: " + str(data))
            await ws.send(data)


async def action_ws_send(jsondata: Dict):
    for iws in wsclients.copy():
        try:
            await iws.send(js.dumps(jsondata))
        except Exception as ex:
            logger.error("Failed to send the alert via WS! " + str(ex))
            wsclients.remove(iws)


def add_timezone_info(jsondata: Dict):
    """
        Fixing the JSON data

        Converts the timestamp string given in UTC string to
        a local timezone based timestamp given in seconds.
        Also converts the direction field to uppercase and appends
        the utc_offset into the JSON object.
    """
    try:
        local_time_zone = timezone(app.config.TIMEZONE)
        t = time.strptime(jsondata["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
        dt = datetime(t.tm_year, t.tm_mon, t.tm_mday,
                      t.tm_hour, t.tm_min, t.tm_sec)
        utc_offset = local_time_zone.utcoffset(dt).total_seconds()
        timestamp = dt.timestamp() + utc_offset
    except Exception as ex:
        logger.error(str(ex))
        raise ex
    jsondata["utcoffset"] = utc_offset
    jsondata["timestamp"] = int(timestamp)


def format_json_input(jsondata: Dict):
    """
        Data format processing

        - strategy direction conversion to uppercase
    """
    jsondata["direction"] = jsondata["direction"].upper()


@app.after_server_stop
def teardown():
    """
        Application shutdown

        Cleanup after server shutdown.
    """
    logger.debug("Closing the Carbon socket...")
    sock = Sanic.get_app().ctx.carbon_sock
    try:
        del sock
    except:
        logger.error("Carbon connection close failed!")


if __name__ == '__main__':
    app.run(host="127.0.0.1",
            port=app.config.PORT,
            dev=app.config.DEV,
            fast=not app.config.DEV,
            access_log=app.config.DEV,
            )
