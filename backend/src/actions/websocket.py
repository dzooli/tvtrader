"""
    Websocket related actions

    File:       websocket.py
    Author:     Zoltan Fabian <zoltan.dzooli.fabian@gmail.com>
"""
import json as js
from sanic.log import logger


async def send_metric(jsondata: dict, clients: set):
    """Send the data to the connected websockets

    Args:
        jsondata (dict): Data to send
        clients (set): Websocket client list
    """
    for iws in clients.copy():
        try:
            await iws.send(js.dumps(jsondata))
        except Exception as ex:
            logger.error("Failed to send the alert via WS! %s", str(ex))
            clients.remove(iws)
