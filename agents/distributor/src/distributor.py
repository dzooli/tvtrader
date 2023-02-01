import ws4py
import wsaccel
import logging

from ws4py.client.threadedclient import WebSocketClient


class DistributorClient(WebSocketClient):
    def __init__(self, *args, **kwargs):
        self._logger = None
        WebSocketClient.__init__(self, *args, **kwargs)

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    def opened(self):
        self._logger.info("WS opened successfully")

    def closed(self, code, reason=None):
        print(f"Closed down: {code}, {reason}")

    def received_message(self, m):
        print(f"{m}")
        if len(m) >= 175:
            self.close(reason="Bye bye")


if __name__ == "__main__":
    applog = logging.getLogger()
    wsaccel.patch_ws4py()
    try:
        ws = DistributorClient(
            "wss://api.gemini.com/v1/marketdata/BTCUSD", protocols=["http-only", "chat"]
        )
        ws.logger = applog
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
