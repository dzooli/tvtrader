"""
Targets for the message distribution

"""


class TargetConnector:
    def __init__(self):
        self._target_connection = None
        self._initialized: bool = False

    def __del__(self):
        if self._initialized and hasattr(self._target_connection, "close"):
            self._target_connection.close()
        del self._target_connection
