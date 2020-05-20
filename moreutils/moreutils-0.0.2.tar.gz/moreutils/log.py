"""
Since initializing loggers is tedious, I use this pattern to create a logger
with an optional stream, file, rotating file, and time based interval file
logger.

This also adds a useful decorator and context manager `logger.log_error` which
allows you to log exceptions that might have been raised. It can be used as
a decorator or a context manager. The context manager can optional ignore
exceptions and continue running the code, if it isn't essential for the code
to work.

Simply add this to the top of your module::

    from moreutils import create_logger

    logger = create_logger(
        stream_level='info',
        file_level='debug',
        log_path='./app.log',
    )

`log_error` can be used like so::

    with logger.log_error('my message'):
        print('logs exceptions that might be raised')

    # or as a decorator

    @logger.log_error
    def myfunc(...):
        pass
"""
import logging
from functools import wraps
from contextlib import contextmanager


def add_log_error(log):
    """
    Adds a new function `log_error` to your logger.
    This can be used as a function decorator like so::

        @log.log_error
        def func(...):
            pass

    Which will have it `log.exception` on any function you decorate.

    It can be used as a context manager as well::

        with log.log_error('my message'):
            ...

    That will `log.exception` any code inside. You can optionally pass
    `reraise=False` to have it continue without raising an exception if the
    code inside can fail and continue, but it defaults to `reraise=True`::

        with log.log_error('my message', reraise=False):
            code_that_does_not_need_to_run_without_errors(...)

    If you use `create_logger` it will automatically add this function to your
    logger.
    """

    @contextmanager
    def log_error_ctx(msg, reraise=True):
        try:
            yield
        except Exception:
            log.exception(msg)
            if reraise:
                raise

    def log_error_deco(func):

        @wraps(func)
        def decorated(*fargs, **fkwargs):
            with log_error_ctx(func.__qualname__):
                return func(*fargs, **fkwargs)

        return decorated

    def log_error(*args, **kwargs):
        if callable(args[0]):
            return log_error_deco(args[0])
        return log_error_ctx(*args, **kwargs)

    log.log_error = log_error
    return log


def create_logger(
    name,
    stream_level=None,
    file_level=None,
    log_path=None,
    when=None,
    utc=None,
    max_mb=None,
    backup_count=None,
    format=None,
    config_data=None,
):
    """
    :name: the name of the logger, usually module `__name__`
    :stream_level: a choice of None, 'debug', 'info', 'warning', 'error', or
        'critical'
        Passing a value other than None will have it add this handler.
    :file_level: a choice of None, 'debug', 'info', 'warning', 'error', or
        'critical'
        If you pass log_path but no file_level, it will default to 'debug'.
        If you pass file_level but no log_path, it will default to
        './{name}.log'
    :log_path: the file path to the desired log file.
        If you pass log_path but no file_level, it will default to 'debug'.
        If you pass file_level but no log_path, it will default to
        './{name}.log'
        it not log to file.
    :when: a choice of None, 'S', 'M', 'H', 'D', 'W0'-'W6' for
        monday through sunday, 'midnight'.
        Passing this keyword will use the `TimedRotatingFileHandler` for
        the file logging.
    :utc: whether to use UTC for the timed rotating logger
    :max_mb: The maximum megabytes per log file. Passing a value will cause
        it to use the `RotatingFileHandler` for the file handler.
    :backup_count: the maximum number of backup files for the Timed and
        Rotating file handlers.
    :format: the format it logs in, defaults to:
        '%(asctime)s - %(levelname)8s - %(name)s - %(message)s'
    :config_data: The section which contains the config values of the same name
        of the keyword arguments this function takes. It will use the config
        rather than what you pass in through the keywords.
    :return: the logger instance
    """
    default_format = '%(asctime)s - %(levelname)8s - %(name)s - %(message)s'
    if config_data:
        stream_level = config_data.get('stream_level')
        file_level = config_data.get('file_level')
        log_path = config_data.get('log_path')
        max_mb = config_data.get('max_mb')
        backup_count = config_data.get('backup_count')
        format = config_data.get('format', default_format)
    else:
        format = format or default_format

    if when and backup_count is None:
        backup_count = 0

    if log_path and not file_level:
        file_level = logging.DEBUG
    if file_level and not log_path:
        log_path = f'./{name}.log'
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format)
    if isinstance(stream_level, str):
        stream_level = getattr(logging, stream_level.upper())
    if isinstance(file_level, str):
        file_level = getattr(logging, file_level.upper())

    if stream_level:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(stream_level)
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)

    file_handler = None
    if file_level and max_mb:
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=max_mb * 2**20,
            backupCount=backup_count,
        )
    elif file_level and when:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_path,
            when=when,
            backupCount=backup_count or 0,
            utc=utc or False,
        )
    elif file_level:
        file_handler = logging.FileHandler(log_path)
        log.addHandler(file_handler)
    if file_handler:
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
    add_log_error(log)
    return log
