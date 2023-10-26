# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, Future
import concurrent.futures as mod_futures
from typing import TypeVar

from ..base import AbstractDistributorEndpoint

CAbstractDistributionTarget = TypeVar(
    "CAbstractDistributionTarget", bound="AbstractDistributionTarget"
)


class AbstractDistributionTarget(AbstractDistributorEndpoint, metaclass=ABCMeta):
    @abstractmethod
    def on_message(self, message: str):
        self.process(message)

    @abstractmethod
    def process(self, message: str):
        ...


CThreadedDistributionTarget = TypeVar(
    "CThreadedDistributionTarget", bound="ThreadedDistributionTarget"
)


class ThreadedDistributionTarget(AbstractDistributionTarget):
    """ThreadPool based target endpoint."""

    def __init__(self, poolsize: int = 10, initializer: Callable | None = None):
        self._pool = ThreadPoolExecutor(
            poolsize, initializer=initializer if initializer is not None else None
        )

    def open(self):
        pass

    def _check_complete(self, result: Future):
        res = None
        try:
            res = result.result()
        except mod_futures.TimeoutError:
            return self.on_timeout(res)
        except mod_futures.CancelledError:
            return self.on_cancel(res)
        except BaseException as exc:
            return self.on_error(exc)
        self.on_complete(res)

    @abstractmethod
    def on_complete(self, result):
        pass

    @abstractmethod
    def on_timeout(self, result):
        pass

    @abstractmethod
    def on_cancel(self, result):
        pass

    @abstractmethod
    def on_error(self, exception):
        """Callback method for exception raised in the process() call."""
        pass

    def on_message(self, message: str):
        task = self._pool.submit(self.process, message)
        task.add_done_callback(self._check_complete)

    @abstractmethod
    def process(self, message: str):
        pass

    def close(self, code: int = -1, reason: str = ""):
        self._pool.shutdown(wait=True, cancel_futures=False)
        return super().close(code, reason)
