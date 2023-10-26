import sys

from tvt_agents.distributor.target import AbstractDistributionTarget


class ConsoleTarget(AbstractDistributionTarget):
    """Simple console logger target.
    Used for demonstration purposes only.
    """

    def __init__(self):
        self._stream = None
        super().__init__()

    def open(self):
        self._stream = sys.stdout

    def close(self, code: int = -1, reason: str = ""):
        """Not needed to close the console"""

    def on_message(self, message):
        self.process(message)

    def process(self, message: str):
        print(message, file=self._stream)


def create_console_target():
    return ConsoleTarget()
