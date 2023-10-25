import importlib
import logging
import sys
import typing

import click
import ws4py
from click_default_group import DefaultGroup


def setup_logging(level: int = logging.DEBUG):
    res_logger = ws4py.configure_logger(level=level)
    fmt = logging.Formatter(
        "%(asctime)s.%(msecs)03d - %(levelname)s - %(filename)s:%(lineno)s - %(message)s"
    )
    for h in res_logger.handlers:
        h.setFormatter(fmt)
    return res_logger


# # Logging configuration example without ws4py
# logging.basicConfig(
#     format="%(asctime)s.%(msecs)03d - %(levelname)s - %(filename)s:%(lineno)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     level=logging.DEBUG,
# )
# logger = logging.getLogger()

logger = setup_logging()
dist_targets: typing.Set[object] = set()


def collect_dist_targets(src: str = "targets"):
    logger.info("Collecting custom targets...")
    targets_module = importlib.import_module(src, src)
    for name in targets_module.__all__:
        if (
            callable(eval(f"targets_module.{name}"))
            and name.startswith("create_")
            and name.endswith("_target")
        ):
            logger.info(f"Found target: {name}. Registration...")
            try:
                obj = eval(f"targets_module.{name}")()
            except Exception:
                logger.critical(
                    f"Cannot instantiate the distributor target with: {name}"
                )
            logger.info(f"{name} has been registered as {obj}")
            dist_targets.add(obj)


@click.group
def show():
    pass


@show.command
@click.option(
    "--verbose", default=False, help="Display target's documentation if exists."
)
def targets(verbose):
    collect_dist_targets()
    print("\nInitialized targets: ")
    for obj in dist_targets:
        print("-", type(obj), "from module:", obj.__module__)
        if verbose:
            print("  Documentation:")
            print("   ", obj.__doc__)


@click.group(cls=DefaultGroup, default="start", default_if_no_args=True)
def cli():
    pass


@cli.command
def start(src: str = "targets"):
    collect_dist_targets(src)
    logger.info("Starting the distributor...")


# Test for dynamically created targets
if __name__ == "__main__":
    cli.add_command(show)
    cli()
    sys.exit()


# Basic usage without dynamic import
# import wsaccel
# from tvt_agents.distributor import Distributor
# from tvt_agents.distributor.source.websocket import WebSocketSource
# logger = setup_logging()
# def run_loop():
#     wsaccel.patch_ws4py()
#     dist = Distributor()
#     dist.logger = logger
#     ws_source = WebSocketSource(
#         "wss://socketsbay.com/wss/v2/1/demo/",
#         protocols=["http-only", "chat"],
#     )
#     ws_source.logger = logger
#     dist.add_source(ws_source)
#     dist.connect()

#     try:
#         dist.run()
#     except KeyboardInterrupt:
#         dist.shutdown()
