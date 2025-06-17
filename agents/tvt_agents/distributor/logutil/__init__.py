"""
A helper module for flexible logging inside inherited classes.
"""
import logging
from attrs import define, field, validators


@define
class LoggingMixin:
    """Use this logger trait where needed."""

    _logger: logging.Logger | None = field(
        init=True,
        validator=validators.optional(validators.instance_of(logging.Logger)),
    )

    def __init__(self):
        self._logger = None

    @property
    def logger(self):
        """The underlying logger."""
        try:
            return self._logger
        except AttributeError:
            return None

    @logger.setter
    def logger(self, logger: logging.Logger):
        """Set the logger."""
        self._logger = logger

    def log(self, level: int, item) -> bool:
        """Use the logger."""
        try:
            logger_fn = getattr(self._logger, str(logging.getLevelName(level)).lower())
        except AttributeError:
            return False
        logger_fn(item)
        return True
