import logging
import wsaccel

from .distributor import AlertDistributor, WSSource


def loggerConfig() -> logging.Logger:
    logging.basicConfig(level=logging.DEBUG, force=True)
    res = logging.getLogger()
    res.root.name = __package__
    return logging.getLogger()


if __name__ == "__main__":
    logger = loggerConfig()
    logger.info("agents package main started...")

    wsaccel.patch_ws4py()
    dist = AlertDistributor()
    dist.logger = logger
    ws_source = WSSource()
    dist.add_source(ws_source)

    try:
        dist.run()
    except KeyboardInterrupt:
        dist.shutdown()
