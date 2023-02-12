# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""
Source connector declarations for the message distribution

"""

from typing import TypeVar
from abc import abstractmethod, ABCMeta

from ws4py.client.threadedclient import WebSocketClient
from ws4py.exc import HandshakeError

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


class WebSocketSource(AbstractDistributionSource):
    _ws = None
    _logger = None

    def __init__(self, url, **kwargs):
        own_kwargs = ["logger"]
        pass_kwargs = dict([(k, v) for k, v in kwargs.items() if k not in own_kwargs])
        self._ws = WebSocketClient(url, **pass_kwargs)
        self._ws.opened = self.opened
        self._ws.closed = self.closed
        try:
            self._logger = kwargs["logger"]
        except KeyError:
            pass

    def close(self, code=1000, reason=""):
        self._ws.close(code, reason)
        self._ws.closed(code, reason)

    def connect(self):
        if self._logger:
            self._logger.debug(f"{__name__}: connecting to the websocket server...")
        try:
            self._ws.connect()
        except HandshakeError:
            if self._logger:
                self._logger.error("WS connection handshake error!")
        if self._logger:
            self._logger.info("WS connected")

    def opened(self):
        if self._logger:
            self._logger.info("source connected")

    def closed(self, code, reason=None):
        if self._logger:
            self._logger.info(f"connection closed: {reason} ({code})")

    def set_on_message(self, message_function):
        self._ws.received_message = message_function
