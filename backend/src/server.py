from sanic.log import logger
from sanic_ext import openapi
from sanic.response import json
from sanic import Sanic

from typing import Dict
import json as js
import jsonschema
from datetime import datetime
from pytz import timezone
import time

from .config import AppConfig
from .schemas.alerts import AlertSchema, ProcessedAlertSchema


wsclients = set()
app = Sanic("TvTrader", config=AppConfig(),
            configure_logging=True, )


@app.get("/")
@openapi.summary("Healthcheck endpoint")
def check(request):
    return json("HEALTHY " + app.config.APPNAME)


@app.post("/")
@openapi.summary("Alert POST endpoint. This is the endpoint for the Chrome extension.")
async def post(request):
    postData = request.body.decode('utf-8').replace("'", '"')
    logger.debug("POST recv: " + postData)
    # POST JSON decoding
    try:
        jsondata = js.loads(postData)
    except Exception as ex:
        logger.error(str(ex))
        return json({"ERROR": str(ex)}, status=400)
    # JSON validation
    try:
        jsonschema.validate(jsondata, schema=AlertSchema)
    except Exception as ex:
        logger.error(str(ex))
        return json({"ERROR": str(ex)}, status=400)
    # Timestamp conversion
    try:
        local_time_zone = timezone(app.config.TIMEZONE)
        t = time.strptime(jsondata["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
        dt = datetime(t.tm_year, t.tm_mon, t.tm_mday,
                      t.tm_hour, t.tm_min, t.tm_sec)
        utc_offset = local_time_zone.utcoffset(dt).total_seconds()
        timestamp = dt.timestamp() + utc_offset
    except Exception as ex:
        logger.error(str(ex))
        return json({"ERROR": str(ex)}, status=400)
    jsondata["timestamp"] = int(timestamp)
    jsondata["direction"] = jsondata["direction"].upper()
    # Send to Websockets
    await actionWebsocketSend(jsondata)
    # Send to Carbon
    await actionCarbonSend(jsondata, utc_offset)
    # Send response
    return json("OK")


@ app.websocket("/alerts")
async def feed(request, ws):
    logger.debug("ws request: " + str(request))
    wsclients.add(ws)
    while True:
        data = None
        data = await ws.recv()
        if data is not None:
            logger.debug("ws data received: " + str(data))
            await ws.send(data)


async def actionWebsocketSend(jsondata: Dict):
    for iws in wsclients.copy():
        try:
            await iws.send(js.dumps(jsondata))
        except Exception as ex:
            logger.error("Failed to send the alert via WS! " + str(ex))
            wsclients.remove(iws)


async def actionCarbonSend(jsondata: Dict, utc_offset: int):
    # Validation
    try:
        jsonschema.validate(jsondata, schema=ProcessedAlertSchema)
    except Exception as ex:
        logger.error("CarbonSend JSON validation error: " + str(ex))
        return
    # Alert timeout calculation
    config = Sanic.get_app().config
    value = 15 if jsondata["direction"] == "SELL" else 85
    timediff = int(time.time()) - (jsondata["timestamp"] - utc_offset)
    if timediff > (config.GR_TIMEOUT * 60):
        value = 50
    # Message prepare
    msg = f'strat.{jsondata["stratName"]}.{jsondata["interval"]}.{jsondata["symbol"]} {value} {jsondata["timestamp"]}\n'
    logger.debug("Carbon message: " + msg)


if __name__ == '__main__':
    app.run(host="127.0.0.1",
            port=app.config.PORT,
            dev=app.config.DEV,
            fast=not app.config.DEV,
            access_log=app.config.DEV,
            )
