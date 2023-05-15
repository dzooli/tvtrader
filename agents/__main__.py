import logging
import wsaccel
import ws4py
import sys
from pprint import pprint
from importlib import import_module
import click
from click_default_group import DefaultGroup

from tvt_agents.distributor.source import WebSocketSource
from tvt_agents.distributor import Distributor


@click.group(cls=DefaultGroup, default='start', default_if_no_args=True)
def cli():
    pass


@cli.command
def start(src: str = "targets"):
    print('Importing custom targets...')
    targets = import_module(src, src)
    for name in targets.__all__:
        print(name, type(name))
        if callable(eval(f"targets.{name}")) and name.startswith('create_') and name.endswith('_target'):
            print(f"{name} is callable")
            obj = eval(f"targets.{name}")()
            print(obj)


if __name__ == "__main__":
    cli()
    exit()


def setup_logging(level: int = logging.DEBUG):
    res_logger = ws4py.configure_logger(level=level)
    fmt = logging.Formatter("| [%(asctime)s] | %(levelname)8s | %(message)s")
    for h in res_logger.handlers:
        h.setFormatter(fmt)
    return res_logger


def run_loop():
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
