"""Alert distribution specific extension definitions
"""

class DistributorException(BaseException):
    pass

class InvalidDistributionTarget(DistributorException):
    pass

class ConnectionNotDefined(DistributorException):
    pass

class InvalidUrlException(DistributorException):
    pass

class ConnectorNotInitialized(DistributorException):
    msg: str
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = "The distribution target connector is not initialized!"
        
