import logging
import wsaccel
import ws4py

from .distributor.source import WebSocketSource
from .distributor import Distributor


logger = ws4py.configure_logger(level=logging.DEBUG)

if __name__ == "__main__":
    logger.info("agents package main started...")

    wsaccel.patch_ws4py()
    dist = Distributor()
    dist.logger = logger
    ws_source = WebSocketSource(
        "wss://socketsbay.com/wss/v2/1/demo/",
        protocols=["http-only", "chat"],
        logger=logger,
    )
    dist.add_source(ws_source)
    dist.connect()

    try:
        dist.run()
    except KeyboardInterrupt:
        dist.shutdown()
