# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""
Alert distributor with multiple sources and targets

"""
import logging
import queue
from threading import Thread
from attrs import define, field, validators
from time import sleep
from typing import List, TypeVar
from queue import Queue
from .source import AbstractDistributionSource
from .target import AbstractDistributionTarget


CDistributor = TypeVar("CDistributor", bound="Distributor")


@define
class Distributor:
    _shutdown_progress: bool = field(default=False)
    _logger: logging.Logger = field(default=None)
    _queue: Queue = field(factory=Queue)
    _src_threadlist: list = field(factory=list)
    _sources: List[AbstractDistributionSource] = field(factory=list)
    _targets: List[AbstractDistributionTarget] = field(factory=list)
    _send_delay: float = field(default=0.2, validator=validators.gt(0.0))

    @property
    def delay(self):
        return self._send_delay

    @delay.setter
    def delay(self, new_delay: float):
        self._send_delay = new_delay

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger: logging.Logger):
        self._logger = logger

    def add_source(self, src: AbstractDistributionSource):
        self._sources.append(src)
        self._sources[-1].set_on_message(self._thread_enqueue)
        if self._logger:
            self._logger.info("source added")

    def connect_sources(self):
        if self._logger:
            self._logger.debug("connecting sources...")
        for src in self._sources:
            src.connect()

    def connect_targets(self):
        if self._logger:
            self._logger.debug("connecting targets...")
        for tgt in self._targets:
            tgt.open()

    def connect(self):
        self.connect_targets()
        self.connect_sources()

    def add_target(self, tgt: AbstractDistributionTarget):
        self._targets.append(tgt)
        if self._logger:
            self._logger.info("target added")

    def _enqueue(self, message):
        if self._shutdown_progress:
            if self._logger:
                self._logger.info("No new messages accepted, shutdown in progress")
            return
        try:
            self._queue.put_nowait(str(message))
        except queue.Full:
            if self._logger:
                self._logger.error("failed to enqueue the message! Queue is full")
            return
        if self._logger:
            self._logger.info("message enqueued...")

    def _thread_enqueue(self, message):
        if self._shutdown_progress:
            if self._logger:
                self._logger.info("No new messages threaded, shutdown in progress")
            return
        self._src_threadlist.append(Thread(target=self._enqueue, kwargs={"message": message}))
        if self._logger:
            self._logger.debug("Starting equeue thread...")
        self._src_threadlist[-1].start()

    def run(self):
        while True:
            while not self._queue.empty():
                last_msg = self._queue.get()
                self._send_to_all(last_msg)
                self._queue.task_done()
            sleep(self._send_delay)

    def _send_to_all(self, message):
        if self._logger:
            self._logger.debug(
                f"sending message '{message}' to all targets..."
            )
        for tgt in self._targets:
            tgt.send(message)
            if self._logger:
                self._logger.info("message sent")

    def flush(self):
        if self._logger:
            self._logger.info("Flushing the queue...")
        while not self._queue.empty():
            last_msg = self._queue.get()
            self._send_to_all(last_msg)
            self._queue.task_done()

    def shutdown(self):
        self._shutdown_progress = True
        if self._logger:
            self._logger.info("closing sources...")
        for src in self._sources.copy():
            src.close(
                code=AbstractDistributionSource.DISCONNECT_SHUTDOWN,
                reason="shutdown by distributor",
            )

        self.flush()

        if self._logger:
            self._logger.info("closing targets...")
        for tgt in self._targets.copy():
            tgt.close()

        if self._logger:
            self._logger.info("Waiting for queue threads to finish...")
        # shutting down the source queue threads
        for t in self._src_threadlist:
            t.join()
        self._shutdown_progress = False
