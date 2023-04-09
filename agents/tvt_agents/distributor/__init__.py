# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""
Alert distributor with multiple sources and targets

"""
import asyncio
from attrs import define, field, validators
from time import sleep
from typing import List, TypeVar
from collections import deque
from .source import AbstractDistributionSource
from .target import AbstractDistributionTarget


CDistributor = TypeVar("CDistributor", bound="Distributor")


@define
class Distributor:
    _logger = field(default=None)
    _message_counter: int = field(default=0)
    _queue = deque([])
    _sources: List[AbstractDistributionSource] = []
    _targets: List[AbstractDistributionTarget] = []
    _send_delay = field(default=0.2, validator=validators.gt(0.0))

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
        if self._logger:
            self._logger.info("source added")

    def connect_sources(self):
        if self._logger:
            self._logger.debug("connecting sources...")
        for source in self._sources:
            source.connect()

    def connect_targets(self):
        if self._logger:
            self._logger.debug("connecting targets...")
        for target in self._targets:
            target.open()

    def connect(self):
        self.connect_targets()
        self.connect_sources()

    def add_target(self, target: AbstractDistributionTarget):
        self._targets.append(target)
        if self._logger:
            self._logger.info("target added")

    def enqueue(self, message):
        try:
            self._queue.append(str(message))
        except Exception as ex:
            ex.add_note("Enqueue failed")
            raise ex
        self._message_counter += 1
        if self._logger:
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
                    if self._logger:
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
        if self._logger:
            self._logger.info("closing targets...")
        for target in self._targets.copy():
            target.close()
        while True:
            try:
                self._queue.pop()
            except IndexError:
                break
