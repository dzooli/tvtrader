import logging
from ws4py.client.threadedclient import WebSocketClient


class RabbitDistributor(WebSocketClient):
    """Distribute to a RabbitMQ topic exchange"""

    def __init__(self, *args, **kwargs):
        self.logger: logging.Logger = logging.getLogger()
        super().__init__(*args, **kwargs)

    def opened(self):
        self.logger.info("WS opened successfully")

    def closed(self, code, reason=None):
        self.logger.info("Closed down: %d, %d" % (code, reason))

    def received_message(self, message):
        self.logger.info("Message received: %s" % message)
        if len(message) >= 175:
            self.close(reason="Example exited")
