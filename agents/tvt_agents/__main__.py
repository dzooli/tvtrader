import logging
import wsaccel


from .distributor import DistributorClient
from .exception import DistributorException

def loggerConfig() -> logging.Logger:
    logging.basicConfig(level=logging.DEBUG, force=True)
    return logging.getLogger()

if __name__ == "__main__":
    logger = loggerConfig()
    logger.info("agents package main started...")

    wsaccel.patch_ws4py()
    try:
        ws = DistributorClient(
            "wss://api.gemini.com/v1/marketdata/BTCUSD", protocols=["http-only", "chat"]
        )
        ws.logger = logger
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
