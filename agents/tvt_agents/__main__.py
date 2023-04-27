import logging
import wsaccel
import ws4py

from .distributor.source import WebSocketSource
from .distributor import Distributor

logger = None


def setup_logging(level: int = logging.DEBUG):
    res_logger = ws4py.configure_logger(level=level)
    fmt = logging.Formatter("| [%(asctime)s] | %(levelname)8s | %(message)s")
    for h in res_logger.handlers:
        h.setFormatter(fmt)
    return res_logger


if __name__ == "__main__":
    logger = setup_logging()

    wsaccel.patch_ws4py()
    dist = Distributor()
    dist.logger = logger
    ws_source = WebSocketSource(
        "wss://socketsbay.com/wss/v2/1/demo/",
        protocols=["http-only", "chat"],
    )
    ws_source.logger = logger
    dist.add_source(ws_source)
    dist.connect()

    try:
        dist.run()
    except KeyboardInterrupt:
        dist.shutdown()
