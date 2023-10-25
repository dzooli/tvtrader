# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""
Alert distributor with multiple sources and targets

"""
import queue
from queue import Queue
from time import sleep
from threading import Thread
from typing import List, TypeVar
from attrs import define, field, validators

from .source import AbstractDistributionSource
from .target import AbstractDistributionTarget
from .exceptions import QueueEmpty
from .logutil import LoggingMixin


CDistributor = TypeVar("CDistributor", bound="Distributor")


@define
class Distributor(LoggingMixin):
    """
    A message distributor.

    Targets must implement AbstractDistributionTarget and
    sources must implement AbstractDistributionSource.
    """

    _shutdown_progress: bool = field(default=False)
    _queue: Queue = field(factory=Queue)
    _src_threadlist: list[Thread] = field(factory=list)
    _sources: List[AbstractDistributionSource] = field(factory=list)
    _targets: List[AbstractDistributionTarget] = field(factory=list)
    _send_delay: float = field(default=0.2, validator=validators.gt(0.0))

    @property
    def delay(self):
        return self._send_delay

    @delay.setter
    def delay(self, new_delay: float):
        self._send_delay = new_delay

    def add_source(self, src: AbstractDistributionSource):
        self._sources.append(src)
        self._sources[-1].set_on_message(self._thread_enqueue)
        self.logger.info("source added")

    def connect_sources(self):
        self.logger.debug("connecting sources...")
        for src in self._sources:
            src.open()

    def connect_targets(self):
        self.logger.debug("connecting targets...")
        for tgt in self._targets:
            tgt.open()

    def connect(self):
        self.connect_targets()
        self.connect_sources()

    def add_target(self, tgt: AbstractDistributionTarget):
        self._targets.append(tgt)
        self.logger.info("target added")

    def _enqueue(self, message):
        if self._shutdown_progress:
            self.logger.warning("No new messages accepted, shutdown in progress.")
            return
        try:
            self._queue.put_nowait(str(message))
        except queue.Full:
            self.logger.error("failed to enqueue the message! Queue is full.")
            return
        self.logger.info("message enqueued...")

    def _thread_enqueue(self, message):
        if self._shutdown_progress:
            self.logger.warning("No new messages threaded, shutdown in progress.")
            return
        self._src_threadlist.append(
            Thread(target=self._enqueue, kwargs={"message": message})
        )
        self.logger.debug("Starting equeue thread...")
        self._src_threadlist[-1].start()

    def run(self):
        while True:
            try:
                last_msg = self._queue.get(block=False)
            except queue.Empty:
                sleep(self._send_delay)
                continue
            self._distribute_to_all(last_msg)
            self._queue.task_done()
            sleep(self._send_delay)

    def _distribute_to_all(self, message):
        self.logger.debug(f"sending message '{message}' to all targets...")
        for tgt in self._targets:
            tgt.distribute(message)
            self.logger.info("message sent")

    def flush(self):
        self.logger.info("Flushing the queue...")
        while not self._queue.empty():
            last_msg = self._queue.get(block=False)
            self._distribute_to_all(last_msg)
            self._queue.task_done()
            sleep(self._send_delay)

    def shutdown(self):
        self._shutdown_progress = True
        self.logger.info("closing sources...")
        for src in self._sources.copy():
            src.close(
                code=AbstractDistributionSource.DISCONNECT_SHUTDOWN,
                reason="shutdown by distributor",
            )

        self.flush()

        self.logger.info("closing targets...")
        for tgt in self._targets.copy():
            tgt.close()

        self.logger.info("Waiting for queue threads to finish...")
        # shutting down the source queue threads
        for c_thread in self._src_threadlist:
            c_thread.join()
        self._shutdown_progress = False
