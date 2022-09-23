"""
Carbon communication related functions.

File:       carbon.py
Author:     Zoltan Fabian
"""
import socket
from sanic import Sanic
from sanic.log import logger


async def send_metric(metric) -> None:
    """
    Send the message to Carbon using the Sanic application context.
    The context must contain ```carbon_sock``` socket initialized

    Parameters:
        metric:     The formatted carbon metric line
    Returns:
        None
    """
    logger.info("Carbon send action...")
    app = Sanic.get_app()
    sock = app.ctx.carbon_sock
    if isinstance(sock, socket.socket):
        sock.send(bytes(metric.encode()))
        logger.info(f"{metric} sent to Carbon")
    else:
        logger.error("Cannot send alert to Carbon")
