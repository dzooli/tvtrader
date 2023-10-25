# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""
Source connector interface declarations for message distribution

"""
from typing import TypeVar
from abc import abstractmethod, ABCMeta

CAbstractDistributionSource = TypeVar(
    "CAbstractDistributionSource", bound="AbstractDistributionSource"
)


class AbstractDistributionSource(metaclass=ABCMeta):
    """Message source interface."""

    DISCONNECT_SHUTDOWN = 0
    DISCONNECT_LOST = 1
    DISCONNECT_RECONNECT = 2

    @abstractmethod
    def open(self):
        """Opens the connection to the source."""

    @abstractmethod
    def set_on_message(self, message_function):
        """Setup the callback function for incoming messages."""

    @abstractmethod
    def close(self, code=1000, reason=""):
        """Closes the connection to the source."""
