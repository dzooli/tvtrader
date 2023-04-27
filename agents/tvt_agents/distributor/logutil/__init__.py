import logging
from attrs import define, field, validators


@define
class LoggingMixin:
    _logger: logging.Logger = field(default=None, init=True,
                                    validator=validators.optional(validators.instance_of(logging.Logger)))

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger: logging.Logger):
        if issubclass(logger.__class__, logging.Logger):
            self._logger = logger

    def log(self, level: int, item) -> bool:
        if not self._logger:
            return False
        try:
            logger_fn = getattr(self._logger, str(logging.getLevelName(level)).lower())
        except AttributeError:
            return False
        logger_fn(item)
        return True
