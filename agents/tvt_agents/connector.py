"""
Connector declarations for the message distribution

"""
from typing import TypeVar
from abc import abstractmethod, ABCMeta

CAbstractDistributionSource = TypeVar(
    "CAbstractDistributionSource", bound="AbstractDistributionSource"
)
CAbstractDistributionTarget = TypeVar(
    "CAbstractDistributionTarget", bound="AbstractDistributionTarget"
)


class AbstractDistributionSource(metaclass=ABCMeta):
    DISCONNECT_SHUTDOWN = 0
    DISCONNECT_LOST = 1
    DISCONNECT_RECONNECT = 2

    @abstractmethod
    def on_connect(self):
        raise NotImplementedError()

    @abstractmethod
    def on_message(self, message):
        raise NotImplementedError()

    @abstractmethod
    def on_disconnect(self, code, reason=None):
        raise NotImplementedError()


class AbstractDistributionTarget(metaclass=ABCMeta):
    """Abstract base class for distribution targets"""

    @abstractmethod
    def open(self, url: str | None = None, **kwargs):
        """Opens the connection.

        Arguments:
            url: the target connection URL
        Keyword Arguments:
            Specific connection arguments passed to the connector.
        """
        raise NotImplementedError()

    @abstractmethod
    def send(self, message):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        """Closes the connection to the target"""
        raise NotImplementedError()
