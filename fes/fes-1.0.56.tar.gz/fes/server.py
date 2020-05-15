import finac as f
import finac.api as api

import logging
import os

from pyaltt2.config import load_yaml

SERVER_CONFIG_SCHEMA = {
    'type': 'object',
    'properties': {
        'fes': {
            'type': 'object',
            'properties': {
                'key': {
                    'type': 'string'
                },
                'ip-header': {
                    'type': 'string',
                    'format': 'uri'
                },
                'finac': {
                    'type': 'object',
                    'properties': {
                        'db': {
                            'type': 'string'
                        },
                        'db-pool-size': {
                            'type': 'integer',
                            'minimum': 1
                        },
                        'keep-integrity': {
                            'type': 'boolean'
                        },
                        'lazy-exchange': {
                            'type': 'boolean'
                        },
                        'rate-allow-reverse': {
                            'type': 'boolean'
                        },
                        'rate-allow-cross': {
                            'type': 'boolean'
                        },
                        'rate-cache-size': {
                            'type': 'integer',
                            'minimum': 1
                        },
                        'rate-cache-ttl': {
                            'type': 'number',
                            'minimum': 0.001
                        },
                        'full-transaction-update': {
                            'type': 'boolean'
                        },
                        'base-asset': {
                            'type': 'string'
                        },
                        'date-format': {
                            'type': 'string'
                        },
                        'multiplier': {
                            'type': 'number',
                            'minimum': 1,
                            'multipleOf': 10
                        },
                        'restrict-deletion': {
                            'type': 'integer',
                            'minimum': 0,
                            'maximum': 2
                        },
                        'redis-host': {
                            'type': 'string'
                        },
                        'redis-port': {
                            'type': 'integer',
                            'minimum': 1
                        },
                        'redis-db': {
                            'type': 'integer',
                            'minimum': 0
                        },
                        'redis-timeout': {
                            'type': 'number',
                            'minimum': 0.001
                        },
                        'redis-blocking-timeout': {
                            'type': 'number',
                            'minimum': 0.001
                        },
                        'custom-account-types': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'name': {
                                        'type': 'string'
                                    },
                                    'code': {
                                        'type': 'integer'
                                    },
                                    'passive': {
                                        'type': 'boolean'
                                    }
                                },
                                'additionalProperties': False,
                                'required': ['name', 'code']
                            }
                        }
                    },
                    'additionalProperties': False,
                    'required': ['db']
                },
                'gunicorn': {
                    'type': 'object'
                }
            }
        },
    },
    'additionalProperties': False,
    'required': ['fes']
}

__version__ = '1.0.56'

f.core.logger = logging.getLogger('gunicorn.error')
api.logger = f.core.logger

config = load_yaml(os.getenv('FES_CONFIG'), schema=SERVER_CONFIG_SCHEMA)['fes']

fc = config['finac']
for k, v in fc.copy().items():
    if '-' in k:
        fc[k.replace('-', '_')] = v
        del fc[k]
f.init(**config.get('finac', {}))
api.real_ip_header = config.get('ip-header')
api.key = config['key']
app = api.app

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
