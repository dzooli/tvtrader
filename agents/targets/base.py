# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tvt_agents.distributor.target import ThreadedDistributionTarget

class ThreadedBase(ThreadedDistributionTarget):
    def on_complete(self, result):
        return super().on_complete(result)

    def on_cancel(self, result):
        return super().on_cancel(result)

    def on_error(self, exception):
        return super().on_error(exception)

    def on_timeout(self, result):
        return super().on_timeout(result)
