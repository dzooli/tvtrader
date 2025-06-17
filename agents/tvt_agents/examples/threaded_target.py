# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from tvt_agents.distributor.target import ThreadedDistributionTarget  # noqa: E402


class TestThreadedTarget(ThreadedDistributionTarget):
    """Usage example for ThreadedDistributionTarget."""

    def process(self, message: str):
        """Process the message. The main work of the initialized threads."""
        print(message)
        return super().process(message)

    def on_complete(self, result):
        """Does nothing on completed processing."""

    def on_cancel(self, result):
        """Callback for cancelled tasks."""
        print("task cancelled")
        return super().on_cancel(result)

    def on_timeout(self, result):
        """Callback for timeout. Not yet used."""
        print("timed out")
        return super().on_timeout(result)

    def on_error(self, exception: BaseException | None):
        """Callback for exception handling in the process() method."""
        print("not completed, exception:", str(exception))
        return super().on_error(exception)


async def run_example(msgcount: int = 1000):
    """Start the distributor target and send "msgcount" messages to it.

    Args:
        msgcount (int, optional): How many messages should be processed. Defaults to 1000.
    """
    pooltarget = TestThreadedTarget()

    for i in range(0, msgcount):
        await pooltarget.on_message(f"hello world #{i}")

    pooltarget.close()
