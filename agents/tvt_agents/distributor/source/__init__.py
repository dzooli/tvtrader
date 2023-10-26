# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""
Source connector interface declarations for message distribution

"""
from typing import TypeVar
from abc import abstractmethod, ABCMeta
from ..base import AbstractDistributorEndpoint

CAbstractDistributionSource = TypeVar(
    "CAbstractDistributionSource", bound="AbstractDistributionSource"
)


class AbstractDistributionSource(AbstractDistributorEndpoint, metaclass=ABCMeta):
    """Message source interface."""

    DISCONNECT_SHUTDOWN = 0
    DISCONNECT_LOST = 1
    DISCONNECT_RECONNECT = 2

    @abstractmethod
    def set_on_message(self, message_function):
        """Setup the callback function for incoming messages."""
