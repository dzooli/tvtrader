# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""
Source connector declarations for the message distribution

"""

import logging
from typing import TypeVar
from abc import abstractmethod, ABCMeta

from ws4py.client.threadedclient import WebSocketClient
from ws4py.exc import HandshakeError

from ..logutil import LoggingMixin

CAbstractDistributionSource = TypeVar(
    "CAbstractDistributionSource", bound="AbstractDistributionSource"
)


class AbstractDistributionSource(metaclass=ABCMeta):
    DISCONNECT_SHUTDOWN = 0
    DISCONNECT_LOST = 1
    DISCONNECT_RECONNECT = 2

    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def set_on_message(self, message_function):
        ...

    @abstractmethod
    def close(self, code=1000, reason=""):
        ...


class WebSocketSource(AbstractDistributionSource, LoggingMixin):
    _ws = None

    def __init__(self, url, **kwargs):
        self._ws = WebSocketClient(url, **kwargs)
        self._ws.opened = self.opened
        self._ws.closed = self.closed

    def close(self, code=1000, reason=""):
        self._ws.close(code, reason)
        self._ws.closed(code, reason)

    def connect(self):
        self.log(logging.DEBUG, "connecting to the websocket server...")
        try:
            self._ws.connect()
        except HandshakeError:
            self.log(logging.ERROR, "WS connection handshake error!")
        self.log(logging.INFO, "WS connected")

    def opened(self):
        self.log(logging.INFO, "source connected")

    def closed(self, code, reason=None):
        self.log(logging.INFO, f"connection closed: {reason} ({code})")

    def set_on_message(self, message_function):
        self._ws.received_message = message_function
