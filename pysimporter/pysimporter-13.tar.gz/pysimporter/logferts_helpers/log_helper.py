import logging


from os import path, makedirs
from traceback import format_exc
from time import gmtime, strftime


class LogHelper:
    """This class allows to manage logger.

       Sets console log or file log -> Choose the log level. Allows to write log on different log levels.
    """

    def __init__(self, log_dir_path, logger_name=None, filename=None, log_level=None, log_dir_name=None, enable_console_log_mode=False):
        self._filename = filename
        self._log_level = log_level
        self._log_dir_path = log_dir_path
        self._log_dir_name = log_dir_name
        self._enable_console_log_mode = enable_console_log_mode

        self._create_log_directory()
        self._set_logger_preferences()
        self.logger = logging.getLogger(logger_name)

    def _set_logger_preferences(self) -> None:
        """Logger initializing.

        Sets console log mode or file log mode -> Sets filename and log directory if file log mode enabled.

        @:returns: None
        @:rtype: NoneType
        """
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

        numeric_level = getattr(logging, self._log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % self._log_level)

        if self._enable_console_log_mode:
            logging.basicConfig(format=log_format, level=numeric_level)
        else:
            if self._filename:
                filename = '{}/{}.log'.format(self._log_dir_path, self._filename)
            else:
                filename = '{}/{}_{}.log'.format(self._log_dir_path, 'log', strftime("%Y-%m-%d-%H-%M", gmtime()))
            logging.basicConfig(filename=filename, format=log_format, level=numeric_level)

    def write(self, lvl: int, msg: str) -> None:
        """Writes a log message.

        @:param lvl: log level
        @:param msg: message to write
        @:type lvl: int
        @:type msg: str

        Writes a log message with certain log level and message.

        @:returns: None
        @:rtype: NoneType
        """

        if (not msg) and (not lvl):
            msg = '{}'.format(format_exc())
        self.logger.log(lvl, msg)

    def _create_log_directory(self) -> None:
        """Creates log directory.

        @:returns: None
        @:rtype: NoneType
        """

        if not self._log_dir_name:
            self._log_dir_name = 'log'
        self._log_dir_path = path.join(self._log_dir_path, self._log_dir_name)

        if not path.exists(self._log_dir_path):
            makedirs(self._log_dir_path)
