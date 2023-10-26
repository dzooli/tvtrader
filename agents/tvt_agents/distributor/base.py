# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
from abc import ABCMeta, abstractmethod
from typing import TypeVar
from attrs import define

CAbstractDistributorEndpoint = TypeVar(
    "CAbstractDistributorEndpoint", bound="AbstractDistributorEndpoint"
)


@define
class AbstractDistributorEndpoint(metaclass=ABCMeta):
    @abstractmethod
    def open(self):
        ...

    @abstractmethod
    def close(self, code: int = -1, reason: str = ""):
        ...
