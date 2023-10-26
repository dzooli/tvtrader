"""
A helper module for flexible logging inside inherited classes.
"""
import logging
from attrs import define, field, validators


@define
class LoggingMixin:
    """Use this logger trait where needed."""

    _logger: logging.Logger = field(
        init=True,
        validator=validators.optional(validators.instance_of(logging.Logger)),
    )

    @property
    def logger(self):
        """The underlying logger."""
        return self._logger

    @logger.setter
    def logger(self, logger: logging.Logger):
        """Set the logger."""
        if issubclass(logger.__class__, logging.Logger):
            self._logger = logger

    def log(self, level: int, item) -> bool:
        """Use the logger."""
        if not self._logger:
            return False
        try:
            logger_fn = getattr(self._logger, str(logging.getLevelName(level)).lower())
        except AttributeError:
            return False
        logger_fn(item)
        return True
