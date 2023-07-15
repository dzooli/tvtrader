"""
    Main server process

    File:       server.py
    Author:     Zoltan Fabian <zoltan.dzooli.fabian@gmail.com>
"""
from __future__ import annotations

import socket
import time
from multiprocessing import Queue

from textwrap import dedent
from sanic import Sanic, Request, HTTPResponse
from sanic.log import logger
from sanic.response import json
from sanic.worker.manager import WorkerManager
from sanic_ext import validate, openapi as doc
from sanic_ext.exceptions import ValidationError

from .actions import carbon as actions_carbon
from .actions import websocket as actions_ws
from .app import helpers
from .app.context import TvTraderContext
from .config import AppConfig
from .models.alerts import TradingViewAlert
from .models.responses.apidoc import SuccessDoc, Error400Doc

wsclients: set = set()
carbon_connection: socket.socket = socket.socket()
try:
    carbon_connection = socket.create_connection(
        (AppConfig.CARBON_HOST, AppConfig.CARBON_PORT), timeout=30
    )
except ConnectionRefusedError:
    logger.error("[ERROR] Carbon connection is not available!")
except TimeoutError:
    logger.error("[ERROR]: Carbon connection timeout!")

appctx = TvTraderContext()
appctx.carbon_sock = carbon_connection
app: Sanic = Sanic("TvTrader", config=AppConfig(), configure_logging=True, ctx=appctx)
app.ext.openapi.describe(
    "TvTrader API",
    version="1.0.0",
    description=dedent("TradingView alert helper API"),
)


@app.main_process_start
async def main_process_start(current_app):
    current_app.shared_ctx.logger_queue = Queue()


@app.exception(ValidationError, ValueError)
def handle_validation_errors(request: Request, exception) -> HTTPResponse:
    return json(
        body={"description": str(exception), "message": "ERROR", "status": 400},
        status=400,
    )


@app.route("/", methods=["GET"])
@doc.definition(
    tag="Backend",
    summary="Healthcheck endpoint",
    response=SuccessDoc,
)
async def check(request: Request) -> HTTPResponse:
    return json({"status": 200, "message": "HEALTHY " + app.config.APPNAME})


@app.route("/alert", methods=["POST"])
@doc.definition(
    tag="Frontend",
    operation="receiveAlert",
    description="Create an alert and pass it to the websocket",
    body={"application/json": TradingViewAlert.model_json_schema()},
    response=[SuccessDoc, Error400Doc],
)
@validate(json=TradingViewAlert)
async def alert_post(request, body: TradingViewAlert):
    """
    Alert POST endpoint to proxy the alerts to the frontend application.
    """
    jsondata = body.model_dump()
    helpers.add_timezone_info(jsondata, Sanic.get_app())
    helpers.format_json_input(jsondata)
    await actions_ws.send_metric(jsondata, wsclients)
    return json({"status": 200, "message": "OK"})


@app.route("/carbon-alert", methods=["POST"])
@doc.definition(
    tag="Backend",
    operation="forwardAlert",
    description="Create an alert and pass it to the connected Carbon service",
    body={"application/json": TradingViewAlert.model_json_schema()},
    response=[SuccessDoc, Error400Doc],
)
@validate(json=TradingViewAlert)
async def carbon_alert_post(request, body: TradingViewAlert):
    """
    Alert POST endpoint to forward the alerts to a Carbon server.
    """
    jsondata = body.model_dump()
    helpers.add_timezone_info(jsondata, Sanic.get_app())
    helpers.format_json_input(jsondata)
    # Message meaning conversion to numbers
    config = Sanic.get_app().config
    value = (
        config.CARBON_SELL_VALUE
        if jsondata["direction"] == "SELL"
        else config.CARBON_BUY_VALUE
    )
    timediff = int(time.time()) - (jsondata["timestamp"] + jsondata["utcoffset"])
    if timediff > (config.GR_TIMEOUT * 60):
        value = int((config.CARBON_SELL_VALUE + config.CARBON_BUY_VALUE) / 2)
    # Message prepare
    msg = f'strat.{jsondata["name"]}.{jsondata["interval"]}.{jsondata["symbol"]} \
        {value} {jsondata["timestamp"]}\n'
    await actions_carbon.send_metric(msg)
    return json({"status": 200, "message": "OK"})


@doc.exclude(True)
@doc.definition(exclude=True)
@app.websocket("/wsalerts")
async def feed(request, ws):
    """
    Websocket endpoint.

    Websocket endpoint for the connected clients. Clients receive
    all the alerts received by the server via '/alert' POST endpoint.
    """
    logger.debug("ws request: %s", str(request))
    wsclients.add(ws)
    while True:
        data = None
        data = await ws.recv()
        if data is not None:
            logger.debug("ws data received: %s", str(data))
            await ws.send(data)


@app.after_server_stop
def teardown(app, loop):
    """
    Application shutdown

    Cleanup after server shutdown.
    """
    logger.debug("Closing the Carbon socket...")
    sock = Sanic.get_app().ctx.carbon_sock
    try:
        del sock
    except NameError:
        logger.error("Carbon connection close failed!")


WorkerManager.THRESHOLD = 300

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=app.config.PORT,
        dev=app.config.DEV,
        fast=not app.config.DEV,
        access_log=app.config.DEV,
    )
