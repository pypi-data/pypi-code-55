from typing import Optional

from beets.logging import BeetsLogger


class LoggingWrapper:
    __instance = None

    @staticmethod
    def get_instance():
        if not LoggingWrapper.__instance:
            LoggingWrapper.__instance = LoggingWrapper()

        return LoggingWrapper.__instance

    def __init__(self):
        if LoggingWrapper.__instance:
            raise Exception(f"Can not create second instance of {__name__}!")

        self._logger: Optional[BeetsLogger] = None

        LoggingWrapper.__instance = self

    def set_internal_logger(self, logger: BeetsLogger) -> None:
        self._logger = logger

    def set_log_level(self, log_level: str) -> None:
        if self._logger:
            self._logger.setLevel(log_level)

    def debug(self, *args, **kwargs) -> None:
        if self._logger:
            self._logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        if self._logger:
            self._logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs) -> None:
        if self._logger:
            self._logger.info(*args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        if self._logger:
            self._logger.info(*args, **kwargs)
