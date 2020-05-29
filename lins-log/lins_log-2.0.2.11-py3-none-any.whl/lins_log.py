import os
import logging.config


class LogFilter(logging.Filter):
    def filter(self, record):
        record.settings = os.environ.get('NODO')
        record.application = os.environ.get('SERVICO')
        record.empresa = os.environ.get('EMPRESA', 'DEVELOPER')
        return True


LOGGING = {
    'version': 1,
    "disable_existing_loggers": True,
    'filters': {
        'settings_filter': {
            '()': LogFilter,
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'graypy': {
            'host': os.environ.get('GRAYLOG_HOST'),
            'port': int(os.environ.get('GRAYLOG_PORT')),
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

logging.config.dictConfig(LOGGING)

