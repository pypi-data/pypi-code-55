import logging
import os
import logging.config


class LogFilter(logging.Filter):
    def filter(self, record):
        record.settings = os.environ.get('NODO')
        record.application = os.environ.get('SERVICO')
        record.empresa = os.environ.get('EMPRESA', 'DEVELOPER')
        return True


class Log:
    def __init__(self):
        logging.config.dictConfig(LOGGING)

    def info(self, message, *args, **kwargs):
        logging.info(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        logging.error(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        logging.debug(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        logging.warning(message, *args, **kwargs)


LOGGING = {
    'version': 1,
    "disable_existing_loggers": True,
    'filters': {
        'settings_filter': {
            '()': 'lins_log.LogFilter',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'graypy': {
            'host': os.environ.get('GRAYLOG_HOST', '192.168.0.51'),
            'port': int(os.environ.get('GRAYLOG_PORT', 12201)),
            'class': 'graypy.GELFUDPHandler',
            'level_names': True,
            'extra_fields': True
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['graypy', 'console'],
        'filters': ['settings_filter']
    }
}

