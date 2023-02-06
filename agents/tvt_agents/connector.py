"""
Targets for the message distribution

"""
from urllib3.exceptions import LocationParseError
from abc import ABC,abstractmethod
from .exception import InvalidDistributionTarget, ConnectorNotInitialized

class AbstractTargetConnection(ABC):
    """Abstract base class for distribution targets"""
    @abstractmethod
    def close(self):
        """Closes the connection to the target
        """
        pass

    @abstractmethod
    def sendMessage(self, message : str = ""):
        pass

    @abstractmethod
    def open(self, url : str | None = None, **kwargs):
        """Opens the connection.

        Arguments:
            url: the target connection URL
        Keyword Arguments:
            Specific connection arguments passed to the connector.
        """
        pass


class DistributionTarget:
    pass
class DistributionTarget:
    """Target of the distributor agent."""
    def __init__(self):
        self._target_connection : AbstractTargetConnection | None = None
        self._initialized: bool = False
        self._opened : bool = False
        self._uri = ""

    @property
    def connection(self) -> DistributionTarget:
        return self._target_connection
    
    @connection.setter
    def connection(self, conn: AbstractTargetConnection | None = None):
        if conn is None:
            raise InvalidDistributionTarget("The distribution target cannot be None")
        self._target_connection = conn
        self._initialized = True

    def connect(self, uri : str | None = None, **kwargs):
        if not self._initialized:
            raise ConnectorNotInitialized()
        if uri is None:
            raise LocationParseError()
        try:
            self._target_connection.open(url = uri, **kwargs)
        except Exception as ex:
            raise ex
        self._uri = uri
        self._opened = True
        
    def close(self):
        if not self._initialized:
            raise ConnectorNotInitialized
        if not self._opened:
            return
        try:
            self._target_connection.close()
        except Exception as ex:
            raise ex
        self._opened = False

    def __del__(self):
        self.close()
        del self._target_connection

