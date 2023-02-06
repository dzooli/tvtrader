from future import __annotations__
import ws4py
import wsaccel
import logging

from ws4py.client.threadedclient import WebSocketClient

from .connector import DistributionTarget
from .exception import InvalidDistributionTarget, ConnectionNotDefined

class DistributorClient():
    pass
class DistributorClient(WebSocketClient):
    def __init__(self, *args, **kwargs):
        self._logger = None
        self._connection_defined = False
        self._target: DistributionTarget = None
        WebSocketClient.__init__(self, *args, **kwargs)

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    @property
    def target_connector(self) -> DistributionTarget:
        return self._target

    @target_connector.setter
    def target_connector(self, target: DistributionTarget) -> DistributorClient:
        """
        Set the distribution target connector

        Args:
            target (TargetConnector): The connector object for the target.

        Raises:
            InvalidTargetConnectionException: Raised when the connector is not a subclass of TargetConnector
        """
        if not issubclass(target, DistributionTarget):
            raise InvalidDistributionTarget()
        self._target = target
        self._connection_defined = True
        return self

    def opened(self):
        self._logger.info("WS opened successfully")

    def closed(self, code, reason=None):
        self._logger.info(f"Closed down: {code}, {reason}")

    def received_message(self, m):
        if not self._connection_defined:
            raise ConnectionNotDefined("The distribution target is not defined!")
        print(f"{m}")
        if len(m) >= 175:
            self.close(reason="Bye bye")
