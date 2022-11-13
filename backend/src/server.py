"""
    Main server process

    File:       server.py
    Author:     Zoltan Fabian <zoltan.dzooli.fabian@gmail.com>
"""
from __future__ import annotations
from multiprocessing import Queue
import time
import socket
import attrs

from sanic.worker.manager import WorkerManager
from sanic.log import logger
from sanic_ext import validate, Config
from sanic_ext.exceptions import ValidationError
from sanic_openapi import openapi2_blueprint, doc
from sanic.response import json
from sanic import Sanic, Request, HTTPResponse

from src.config import AppConfig
from src.app.context import TvTraderContext
from src.schemas.alerts import TradingViewAlert, TradingViewAlertSchema
from src.schemas.responses import SuccessResponseSchema, ErrorResponseSchema
import src.actions.carbon as actions_carbon
import src.actions.websocket as actions_ws
import src.app.helpers as helpers


wsclients: set = set()
carbon_connection = None
try:
    carbon_connection = socket.create_connection(
        (AppConfig.CARBON_HOST, AppConfig.CARBON_PORT)
    )
except ConnectionRefusedError:
    logger.error("[ERROR] Carbon connection is not available.")

appctx = TvTraderContext()
appctx.carbon_sock = carbon_connection
app = Sanic("TvTrader", config=AppConfig(), configure_logging=True, ctx=appctx)
app.extend(config=Config(oas=False, health=True, health_endpoint=True, logging=True))
app.blueprint(openapi2_blueprint)


@app.main_process_start
async def main_process_start(app):
    app.shared_ctx.logger_queue = Queue()


@app.exception(ValidationError, ValueError)
def handle_validation_errors(request: Request, exception) -> HTTPResponse:
    """
    Handle validation errors with a proper JSON response.

    Args:
        request (Request): The incoming request
        exception (_type_): Validation exception to handle.

    Returns:
        HTTPResponse: _description_
    """
    return json(body={"description": str(exception), "message": 'ERROR', "status": 400}, status=400)


@app.route("/", methods=["GET"])
@doc.tag("Backend")
@doc.summary("Healthcheck endpoint")
@doc.response(200, SuccessResponseSchema, description="Success")
async def check(request: Request) -> HTTPResponse:
    """
    Healthcheck endpoint.

    Args:
        request (Request): The HTTP request

    Returns:
        HTTPResponse: The health status
    """
    return json({"status": 200, "message": "HEALTHY " + app.config.APPNAME})


@app.route("/alert", methods=["POST"])
@doc.tag("Frontend")
@doc.operation("frontendAlert")
@doc.consumes(TradingViewAlertSchema, location="body")
@doc.response(200, SuccessResponseSchema, description="Success")
@doc.response(
    400,
    ErrorResponseSchema,
    description="Error. See 'description' property in the response",
)
@validate(json=TradingViewAlert)
async def alert_post(request, body: TradingViewAlert):
    """
    Alert POST endpoint to proxy the alerts to the frontend application.
    """
    jsondata = attrs.asdict(body)
    helpers.add_timezone_info(jsondata, Sanic.get_app())
    helpers.format_json_input(jsondata)
    await actions_ws.send_metric(jsondata, wsclients)
    return json({"status": 200, "message": "OK"})


@app.route("/carbon-alert", methods=["POST"])
@doc.tag("Backend")
@doc.operation("carbonAlert")
@doc.consumes(TradingViewAlertSchema, location="body")
@doc.response(200, SuccessResponseSchema, description="Success")
@doc.response(
    400,
    ErrorResponseSchema,
    description="Error. See 'description' property in the response",
)
@validate(json=TradingViewAlert)
async def carbon_alert_post(request, body: TradingViewAlert):
    """
    Alert POST endpoint to forward the alerts to a Carbon server.
    """
    jsondata = attrs.asdict(body)
    helpers.add_timezone_info(jsondata, Sanic.get_app())
    helpers.format_json_input(jsondata)
    # Message meaning conversion to numbers
    config = Sanic.get_app().config
    value = (
        config.CARBON_SELL_VALUE
        if jsondata["direction"] == "SELL"
        else config.CARBON_BUY_VALUE
    )
    timediff = int(time.time()) - \
        (jsondata["timestamp"] + jsondata["utcoffset"])
    if timediff > (config.GR_TIMEOUT * 60):
        value = int((config.CARBON_SELL_VALUE + config.CARBON_BUY_VALUE) / 2)
    # Message prepare
    msg = f'strat.{jsondata["name"]}.{jsondata["interval"]}.{jsondata["symbol"]} \
        {value} {jsondata["timestamp"]}\n'
    await actions_carbon.send_metric(msg)
    return json({"status": 200, "message": "OK"})


@doc.exclude(True)
@doc.route(summary="Websocket endpoint")
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


WorkerManager.THRESHOLD = 300

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=app.config.PORT,
        dev=app.config.DEV,
        fast=not app.config.DEV,
        access_log=app.config.DEV,
    )
