# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
from ws4py.client.threadedclient import WebSocketClient
from ws4py.exc import HandshakeError

from ..logutil import LoggingMixin
from . import AbstractDistributionSource


class WebSocketSource(AbstractDistributionSource, LoggingMixin):
    _ws: WebSocketClient

    def __init__(self, url, **kwargs):
        self._ws = WebSocketClient(url, **kwargs)
        self._ws.opened = self.opened
        self._ws.closed = self.closed

    def close(self, code=1000, reason=""):
        self._ws.close(code, reason)
        self._ws.closed(code, reason)

    def open(self):
        self.logger.debug("connecting to the websocket server...")
        try:
            self._ws.connect()
        except HandshakeError:
            self.logger.error("WS connection handshake error!")
        self.logger.info("WS connected")

    def opened(self):
        self.logger.info("source connected")

    def closed(self, code, reason=None):
        self.logger.info(f"connection closed: {reason} ({code})")

    def set_on_message(self, message_function):
        self._ws.received_message = message_function
