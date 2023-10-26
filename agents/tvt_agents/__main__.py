# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


import cProfile
import importlib
import logging
import os
import sys
from time import perf_counter
import click
import ws4py
from click_default_group import DefaultGroup

from tvt_agents.examples.threaded_target import run_example as threaded_example


def setup_logging(level: int = logging.DEBUG):
    res_logger = ws4py.configure_logger(level=level)
    fmt = logging.Formatter(
        "%(asctime)s.%(msecs)03d - %(levelname)s - %(filename)s:%(lineno)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
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
dist_targets = []


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
            logger.info(f"Found target: {name}. Registration...")
            obj = None
            try:
                obj = eval(f"targets_module.{name}")()
            except Exception:
                logger.critical(
                    f"Cannot instantiate the distributor target with: {name}"
                )
            if obj:
                logger.info(f"{name} has been registered as {obj}")
                logger.debug(type(obj))
                if obj not in dist_targets:
                    dist_targets.append(obj)
                logger.debug(f"target count: {len(dist_targets)}")
            else:
                logger.error("registration failed!")


@click.group
def show():
    """Show various internal information."""


@click.group
def example():
    """Run selected example."""


@click.group
def profile():
    """Profile a selected example."""


@click.group
def timing():
    """Get timing information of the selected example."""


@example.command
@click.option("--count", default=1000, help="Number of messages to process.")
def threadedtarget(count: int):
    """Run the example for ThreadedDistributionTarget."""
    threaded_example()


@profile.command
@click.option("--count", default=1000, help="Number of messages to process.")
def threadedtarget(count: int):
    """Profile the example for ThreadedDistributionTarget."""
    func = f"threaded_example({count})"
    cProfile.run(func)


@timing.command
@click.option("--count", default=1000, help="Number of messages to process.")
def threadedtarget(count: int):
    """Measure execution time of ThreadedDistributionTarget."""
    start_time = perf_counter()
    threaded_example(count)
    print(f"Elapsed time: {(perf_counter() - start_time):0.6f}")


@show.command
@click.option(
    "--verbose",
    default=False,
    is_flag=True,
    help="Display target's documentation if exists.",
)
def targets(verbose):
    """Show loaded distribution targets"""
    collect_dist_targets()
    print("\nInitialized targets: ")
    for obj in dist_targets:
        print("-", type(obj), "from module:", obj.__module__)
        if verbose:
            print("  Documentation:")
            print("   ", obj.__doc__)


@click.group(cls=DefaultGroup, default="start", default_if_no_args=True)
def cli():
    """CLI for distributed agents."""


@cli.command
def start(src: str = "targets"):
    collect_dist_targets(src)
    logger.info("Starting the distributor...")


def main():
    cli.add_command(show)
    cli.add_command(example)
    cli.add_command(profile)
    cli.add_command(timing)
    cli()


# Test for dynamically created targets
if __name__ == "__main__":
    main()
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
