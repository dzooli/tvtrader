"""
Alert distributor with multiple sources and targets

"""
from time import sleep
from typing import List
from collections import deque
from .connector import AbstractDistributionTarget, AbstractDistributionSource


from ws4py.client.threadedclient import WebSocketClient
from ws4py.exc import HandshakeError


class WSSource(AbstractDistributionSource):
    _ws = None
    _logger = None

    def __init__(self, url, **kwargs):
        own_kwargs = ["logger"]
        pass_kwargs = dict([(k, v) for k, v in kwargs.items() if k not in own_kwargs])
        self._ws = WebSocketClient(url, **pass_kwargs)
        self._ws.opened = self.opened
        self._ws.closed = self.closed
        if "logger" in kwargs.keys():
            self._logger = kwargs["logger"]

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
            self._logger.info(f"connection closed: {reason}")

    def set_on_message(self, message_function):
        self._ws.received_message = message_function


class AlertDistributor:
    def __init__(self, delay: float = 0.2):
        self._logger = None
        self._counter = 0
        self._queue = deque([])
        self._sources: List[AbstractDistributionSource] = []
        self._targets: List[AbstractDistributionTarget] = []
        self._send_delay = delay

    @property
    def delay(self):
        return self._send_delay

    @delay.setter
    def delay(self, new_delay: float):
        if new_delay < 0.0:
            raise ValueError
        self._send_delay = new_delay

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    def add_source(self, source: AbstractDistributionSource):
        self._sources.append(source)
        self._sources[-1].set_on_message(self.enqueue)
        if self.logger:
            self._logger.info("source added")

    def add_target(self, target: AbstractDistributionTarget):
        self._targets.append(target)
        if self.logger:
            self._logger.info("target added")

    def enqueue(self, message):
        self._queue.append(str(message))
        if self.logger:
            self._logger.info("message enqueued...")

    def run(self):
        while True:
            if len(self._queue):
                last_msg = self._queue.pop()
                if self._logger:
                    self._logger.debug(
                        f"sending message '{last_msg}' to all targets..."
                    )
                for target in self._targets:
                    target.send(last_msg)
                    if self.logger:
                        self._logger.info("message sent")
            sleep(self._send_delay)

    def shutdown(self):
        if self._logger:
            self._logger.info("closing sources...")
        for source in self._sources.copy():
            source.close(
                code=AbstractDistributionSource.DISCONNECT_SHUTDOWN,
                reason="shutdown by distributor",
            )
        for target in self._targets.copy():
            target.close()
        while True:
            try:
                self._queue.pop()
            except IndexError:
                break
