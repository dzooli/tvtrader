import sys

from tvt_agents.distributor.target import AbstractDistributionTarget


class ConsoleTarget(AbstractDistributionTarget):
    def __init__(self):
        self._stream = None

    def open(self, url: str | None = None, **kwargs):
        self._stream = sys.stdout

    def close(self):
        pass

    def send(self, message):
        print(message)


def create_console_target():
    return ConsoleTarget()
