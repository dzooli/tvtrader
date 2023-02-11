from time import sleep
from typing import List
from .connector import AbstractDistributionTarget, AbstractDistributionSource

from ws4py.client.threadedclient import WebSocketClient


class WSSource(AbstractDistributionSource):
    def on_connect(self):
        return super().on_connect()

    def on_disconnect(self, code, reason=None):
        return super().on_disconnect(code, reason)

    def on_message(self, message):
        return super().on_message(message)


class AlertDistributor:
    def __init__(self):
        self._logger = None
        self._counter = 0
        self._queue = []
        self._sources: List[AbstractDistributionSource] = []
        self._targets: List[AbstractDistributionTarget] = []

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    def add_source(self, source: AbstractDistributionSource):
        self._sources.append(source)
        self._sources[-1].on_message = self.enqueue
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

    def run(self, sleep_sec=0.5):
        while True:
            no_message = False
            try:
                last_msg = self._queue.pop()
            except IndexError:
                no_message = True
            if not no_message:
                for target in self._targets:
                    target.send(last_msg)
                    if self.logger:
                        self._logger.info("message sent")
            sleep(sleep_sec)

    def shutdown(self):
        for source in self._sources.copy():
            source.on_disconnect(
                AbstractDistributionSource.DISCONNECT_SHUTDOWN, "shutdown by runner"
            )
        for target in self._targets.copy():
            target.close()
        while True:
            try:
                self._queue.pop()
            except IndexError:
                break
