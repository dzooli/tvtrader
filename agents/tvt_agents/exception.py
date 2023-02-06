"""Alert distribution specific extension definitions
"""

class DistributorException(BaseException):
    pass

class InvalidTargetConnectionException(DistributorException):
    pass

class ConnectionNotDefined(DistributorException):
    pass
