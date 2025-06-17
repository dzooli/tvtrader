# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import importlib
import logging
import os
import sys
from time import perf_counter

from pprint import pprint
from urllib3 import util as url_util
import asyncclick as click
import ws4py
import wsaccel

from tvt_agents.distributor import Distributor
from tvt_agents.distributor.source.websocket import WebSocketSource
from tvt_agents.examples.threaded_target import run_example as threaded_example

DEFAULT_LOG_LEVEL="DEBUG"
DEFAULT_LOG_INT = -1
try:
    DEFAULT_LOG_INT=logging.getLevelNamesMapping()[DEFAULT_LOG_LEVEL]
except KeyError:
    print(f"Invalid default log level! ({DEFAULT_LOG_LEVEL})")
    sys.exit(1)

dist_targets = []

def setup_logging(level: int = logging.DEBUG):
    res_logger = ws4py.configure_logger(level=level)
    fmt = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] REL:%(relativeCreated)d - PID:%(process)d - %(levelname)s - %(module)s:%(filename)s:%(lineno)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    for h in res_logger.handlers:
        h.setFormatter(fmt)
    return res_logger


logger = setup_logging(DEFAULT_LOG_INT)


def collect_dist_targets(src: str = "targets"):
    """Collecting the distribution target modules.

    Args:
        src (str, optional): Directory relative to the script from where target plugins should be loaded. Defaults to "targets".
    """
    logger.info(f"Path: {os.getcwd()}")
    logger.debug("Appending $PWD to module search path...")
    sys.path.append(".")
    logger.info("Collecting custom targets...")
    targets_module = importlib.import_module(src, src)
    for name in targets_module.__all__:
        if (
            callable(eval(f"targets_module.{name}"))
            and name.startswith("create_")
            and name.endswith("_target")
        ):
            logger.info(f"Found target factory: {name}. Registration...")
            obj = None
            try:
                obj = eval(f"targets_module.{name}")()
            except Exception:
                logger.critical(
                    f"Cannot instantiate the distributor target with: {name}"
                )
            if obj:
                logger.info(f"{obj} has been registered by {name}")
                logger.debug(type(obj))
                if obj not in dist_targets:
                    dist_targets.append(obj)
                logger.debug(f"target count: {len(dist_targets)}")
            else:
                logger.error("registration failed!")


@click.group
def example():
    """Run selected example."""


@example.command
@click.option("--count", default=1000, help="Number of messages to process.")
async def threadedtarget(count: int):
    """Run the example for ThreadedDistributionTarget."""
    await threaded_example(count)


@click.group
def timing():
    """Get timing information of the selected example."""


@timing.command
@click.option("--count", default=1000, help="Number of messages to process.")
@click.option(
    "--log_level",
    type=click.Choice(
        ["DEBUG", "ERROR", "WARNING", "INFO", "CRITICAL"], case_sensitive=False
    ),
    default=DEFAULT_LOG_LEVEL,
    help="Set logging level.",
)
async def threadedtarget(count: int, log_level):
    """Measure execution time of ThreadedDistributionTarget."""
    logger.setLevel(log_level)
    start_time = perf_counter()
    await threaded_example(count)
    print(f"Elapsed time: {(perf_counter() - start_time):0.6f}")


@click.group
def show():
    """Show various internal information."""


@show.command
@click.option(
    "--verbose",
    default=False,
    is_flag=True,
    help="Display target's documentation if exists.",
)
@click.option(
    "--log_level",
    type=click.Choice(
        ["DEBUG", "ERROR", "WARNING", "INFO", "CRITICAL"], case_sensitive=False
    ),
    default=DEFAULT_LOG_LEVEL,
    help="Set logging level.",
)
def targets(verbose, log_level):
    """Show loadable distribution targets"""
    logger.setLevel(log_level)
    collect_dist_targets()
    print("\nInitialized targets: ")
    for obj in dist_targets:
        print("-", type(obj), "from module:", obj.__module__)
        if verbose:
            print("  Documentation:")
            print("   ", obj.__doc__)


@click.group
def cli():
    """CLI for distributed trading agents."""


async def run_websocket_source_loop(logger, websocket_url: str | None = None):
    if not websocket_url:
        logger.error("WS source not specified!")
        raise ValueError
    wsaccel.patch_ws4py()
    dist = Distributor(logger)
    dist.logger = logger
    ws_source = WebSocketSource(
        websocket_url,
        protocols=["http-only", "chat"],
    )
    ws_source.logger = logger
    dist.add_source(ws_source)
    for target in dist_targets:
        target.logger = logger
        dist.add_target(target)
    dist.connect()

    try:
        await dist.run()
    except KeyboardInterrupt:
        await dist.shutdown()


def validate_url_scheme(url: str, req_scheme: str = "ws") -> bool:
    logger.info("Validating URL scheme...")
    p_url = url_util.parse_url(url)
    return isinstance(p_url, url_util.Url) and isinstance(p_url.scheme, str) and p_url.scheme.startswith(req_scheme)


@cli.command
@click.option(
    "--log_level",
    type=click.Choice(
        ["DEBUG", "ERROR", "WARNING", "INFO", "CRITICAL"], case_sensitive=False
    ),
    default=DEFAULT_LOG_LEVEL,
    help="Set logging level.",
)
@click.option(
    "--src", default="targets", help="Directory for dynamic target modules."
)
@click.option('--ws_url', default="wss://socketsbay.com/wss/v2/1/demo/", help="Websocket distribution source URL.")
async def start(src: str, log_level: str, ws_url: str):
    """Start the distributor with WS source and targets from [src] directory.

    src: is './targets' by default.

    Each dynamic target module must define a create_<targetname>_target() function to be detectable as a target module.
    """
    logger.setLevel(log_level)
    collect_dist_targets(src)
    if not validate_url_scheme(ws_url):
        click.secho("Invalid ws_url!", fg="red")
        return
    logger.info("Starting the distributor...")
    await run_websocket_source_loop(logger, ws_url)


def main():
    cli.add_command(show)
    cli.add_command(example)
    cli.add_command(timing)
    cli()


if __name__ == "__main__":
    main()
    sys.exit()
