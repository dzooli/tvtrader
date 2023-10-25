import sys

from tvt_agents.distributor.target import AbstractDistributionTarget


class ConsoleTarget(AbstractDistributionTarget):
    """Simple console logger target.
    Used for demonstration purposes only.
    """

    def __init__(self):
        self._stream = None

    def open(self):
        self._stream = sys.stdout

    def close(self):
        pass

    def distribute(self, message):
        print(message)


def create_console_target():
    return ConsoleTarget()
