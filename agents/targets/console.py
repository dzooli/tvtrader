import sys

from tvt_agents.distributor.logutil import LoggingMixin

from .base import ThreadedBase

class ConsoleTarget(ThreadedBase, LoggingMixin):
    """Simple console logger target.
    Used for demonstration purposes only.
    """

    def __init__(self):
        self._stream = None
        LoggingMixin.__init__(self)
        super().__init__()

    def open(self):
        self._stream = sys.stdout

    async def on_message(self, message: str):
        if self.logger:
            self.logger.debug("starting thread for processing the message...")
        return await super().on_message(message)

    def process(self, message: str):
        if self.logger:
            self.logger.debug(type(self))
        print(type(self), ":", message, file=self._stream)


def create_console_target():
    return ConsoleTarget()
