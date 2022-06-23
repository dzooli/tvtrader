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
from .schemas.alerts import AlertSchema


wsclients = set()
app = Sanic("TvTrader", config=AppConfig(),
            configure_logging=True, )


@app.get("/")
@openapi.summary("Healthcheck endpoint")
def check(request):
    return json("HEALTHY " + app.config.APPNAME)


@ app.post("/alert")
async def alert_post(request):
    """
    Alert POST endpoint to proxy the alerts to the frontend application."

    openapi:
    ---
    operationId: carbonAlert
    parameters:
      - name: data
        in: body
        description: JSON encoded alert
        required: true
        schema:
          type: object
          required:
            - stratId
          properties:
            stratId:
              type: number
            stratName:
              type: string
            symbol:
              type: string
            direction:
              type: string
              description: Direction of the alerted trade opportunity
            interval:
              type: string
              description: The resolution of the chart
            timestamp:
              type: string
    responses:
        '200':
          description: Everything is ok
        '400':
          description: Some error happened. See the ERROR porperty of the response object.
    """
    try:
        jsondata = get_jsondata(request)
        validate_post(jsondata, AlertSchema)
        fix_jsondata(jsondata)
    except Exception as ex:
        return json({"ERROR": str(ex)}, status=400)
    await actionWebsocketSend(jsondata)
    return json("OK")


@ app.post("/carbon-alert")
async def carbon_alert_post(request):
    """
    Alert POST endpoint to proxy the alerts to a Carbon server."

    openapi:
    ---
    operationId: carbonAlert
    parameters:
      - name: data
        in: body
        description: JSON encoded alert
        required: true
        schema:
          type: object
          required:
            - stratId
          properties:
            stratId:
              type: number
            stratName:
              type: string
            symbol:
              type: string
            direction:
              type: string
            interval:
              type: string
              description: The resolution of the chart
            timestamp:
              type: string
    responses:
        '200':
          description: Everything is ok
        '400':
          description: Some error happened. See the ERROR porperty of the response object.
    """
    try:
        jsondata = get_jsondata(request)
        validate_post(jsondata, AlertSchema)
        fix_jsondata(jsondata)
    except Exception as ex:
        return json({"ERROR": str(ex)}, status=400)
    # Message meaning conversion to numbers
    config = Sanic.get_app().config
    value = 15 if jsondata["direction"] == "SELL" else 85
    timediff = int(time.time()) - \
        (jsondata["timestamp"] - jsondata["utcoffset"])
    if timediff > (config.GR_TIMEOUT * 60):
        value = 50
    # Message prepare
    msg = f'strat.{jsondata["stratName"]}.{jsondata["interval"]}.{jsondata["symbol"]} {value} {jsondata["timestamp"]}\n'
    logger.debug("Carbon message: " + msg)
    return json("OK")


@ app.websocket("/wsalerts")
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


def get_jsondata(request):
    postData = request.body.decode('utf-8').replace("'", '"')
    logger.debug("POST recv: " + postData)
    try:
        jsondata = js.loads(postData)
    except Exception as ex:
        logger.error(str(ex))
        raise ex
    return jsondata


def validate_post(jsondata: Dict, schema: Dict):
    try:
        jsonschema.validate(jsondata, schema=schema)
    except Exception as ex:
        logger.error(str(ex))
        raise ex


def fix_jsondata(jsondata: Dict):
    """
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
    jsondata["direction"] = jsondata["direction"].upper()


if __name__ == '__main__':
    app.run(host="127.0.0.1",
            port=app.config.PORT,
            dev=app.config.DEV,
            fast=not app.config.DEV,
            access_log=app.config.DEV,
            )
