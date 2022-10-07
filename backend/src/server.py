from sanic.log import logger
from sanic_ext import validate
from sanic_ext import Config
from sanic_openapi import openapi2_blueprint, doc
from sanic.response import json
from sanic import Sanic
import time
import socket
import attrs

from src.config import AppConfig
from src.app.context import TvTraderContext
from src.schemas.alerts import TradingViewAlert, TradingViewAlertSchema
from src.schemas.response_error import ErrorResponseSchema
import src.actions.carbon as actions_carbon
import src.actions.websocket as actions_ws
import src.app.helpers as helpers


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
app.extend(config=Config(oas=False))
app.blueprint(openapi2_blueprint)


@app.get("/")
@doc.tag("Backend")
@doc.summary("Healthcheck endpoint")
@doc.response(200, {"status": int, "message": str})
def check(request):
    return json({"status": 200, "message": "HEALTHY " + app.config.APPNAME})


@app.post("/alert")
@doc.tag("Frontend")
@doc.operation("frontendAlert")
@doc.consumes(TradingViewAlertSchema, location="body")
@doc.response(200, "OK", description="Success")
@doc.response(500, ErrorResponseSchema, description="Error occurred. See 'message' property in the response")
@validate(json=TradingViewAlert)
async def alert_post(request, body: TradingViewAlert):
    """
    Alert POST endpoint to proxy the alerts to the frontend application.
    """
    try:
        jsondata = attrs.asdict(body)
        helpers.add_timezone_info(jsondata, Sanic.get_app())
        helpers.format_json_input(jsondata)
    except Exception as ex:
        return json({"ERROR": str(ex)}, status=400)
    await actions_ws.send_metric(jsondata, wsclients)
    return json("OK")


@app.post("/carbon-alert")
@doc.tag("Backend")
@doc.operation("carbonAlert")
@doc.consumes(TradingViewAlertSchema, location="body")
@doc.response(200, "OK", description='Success')
@doc.response(500, ErrorResponseSchema, description="Error occurred. See 'message' property in the response")
@validate(json=TradingViewAlert)
async def carbon_alert_post(request, body: TradingViewAlert):
    """
        Alert POST endpoint to forward the alerts to a Carbon server.
    """
    try:
        jsondata = attrs.asdict(body)
        helpers.add_timezone_info(jsondata, Sanic.get_app())
        helpers.format_json_input(jsondata)
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
    await actions_carbon.send_metric(msg)
    return json("OK")


@doc.exclude(True)
@doc.route(summary="Websocket endpoint")
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
    except Exception:
        logger.error("Carbon connection close failed!")


if __name__ == '__main__':
    app.run(host="127.0.0.1",
            port=app.config.PORT,
            dev=app.config.DEV,
            fast=not app.config.DEV,
            access_log=app.config.DEV,
            )
