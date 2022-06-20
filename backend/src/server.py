from sanic.log import logger
from sanic_ext import openapi
from sanic.response import json
from sanic import Sanic

import json as js
import jsonschema
from datetime import datetime
from pytz import timezone
import time

from .config import AppConfig


wsclients = set()
app = Sanic("TvTrader", config=AppConfig(),
            configure_logging=True, )


@app.get("/")
@openapi.summary("Healthcheck endpoint")
def check(request):
    return json("HEALTHY " + app.config.APPNAME)


AlertSchema = {
    "type": "object",
    "required": ["stratId", "stratName", "symbol", "direction", "timestamp", "interval"],
    "properties": {
        "stratId":      {"type": "number", "minimum": 0},
        "stratName":    {"type": "string"},
        "symbol":       {"type": "string"},
        "interval":     {"type": "number"},
        "direction":    {"type": "string", "maxLength": 4},
        "timestamp":    {"type": "string"}
    }
}


@app.post("/")
@openapi.summary("Alert POST endpoint. This is the endpoint for the Chrome extension.")
async def post(request):
    app = Sanic.get_app()

    try:
        jsondata = js.loads(request.body.decode('utf-8').replace("'", '"'))
    except Exception as ex:
        return json({"ERROR": str(ex)}, status=400)
    try:
        jsonschema.validate(jsondata, schema=AlertSchema)
    except Exception as ex:
        return json({"ERROR": str(ex)}, status=400)

    try:
        local_time_zone = timezone(app.config.TIMEZONE)
        t = time.strptime(jsondata["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
        dt = datetime(t.tm_year, t.tm_mon, t.tm_mday,
                      t.tm_hour, t.tm_min, t.tm_sec)
        utc_offset = local_time_zone.utcoffset(dt).total_seconds()
        timestamp = dt.timestamp() + utc_offset
    except Exception as ex:
        return json({"ERROR": str(ex)}, status=400)
    jsondata["timestamp"] = int(timestamp)
    jsondata["direction"] = jsondata["direction"].upper()

    for iws in wsclients.copy():
        try:
            await iws.send(js.dumps(jsondata))
            logger.info("POST data sent to WS: " + js.dumps(jsondata))
        except Exception as ex:
            logger.error("Failed to send the alert via WS! " + str(ex))
            wsclients.remove(iws)
    return json("OK")


@ app.websocket("/alerts")
async def feed(request, ws):
    app = Sanic.get_app()
    logger.info("ws request: " + str(request))
    wsclients.add(ws)
    while True:
        data = None
        data = await ws.recv()
        if data is not None:
            if app.config.DEV:
                logger.info("ws data received: " + str(data))
            await ws.send(data)


if app.config.DEV:
    if __name__ == '__main__':
        app.run(host="127.0.0.1",
                port=app.config.PORT,
                dev=app.config.DEV,
                fast=not app.config.DEV,
                access_log=app.config.DEV,
                workers=4)
else:
    print("Run this app with Uvicorn in production mode!")
    exit()
