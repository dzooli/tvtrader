"""
    Websocket related actions

    File:       websocket.py
    Author:     Zoltan Fabian <zoltan.dzooli.fabian@gmail.com>
"""
import json as js
from typing import Dict, List
from sanic.log import logger


async def send_metric(jsondata: Dict, clients: List):
    for iws in clients.copy():
        try:
            await iws.send(js.dumps(jsondata))
        except Exception as ex:
            logger.error("Failed to send the alert via WS! " + str(ex))
            clients.remove(iws)
