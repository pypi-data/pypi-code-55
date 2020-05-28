import inspect
from time import sleep
from types import FunctionType

import dramatiq
from dramatiq import RateLimitExceeded, Worker
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

import kctaskman.util
import tasks
from lib.util import MS_HOUR
from kctaskman.log import logger

ACTOR_RETRY = 3


def _makeActor(m):
    global __cfgs

    def m1(*req, **kwargs):
        logger.info('task start. actor=%s, req=%s',
                    m.__name__, req)
        retry = 0
        while True:
            try:
                res = m(*req)
            except AbortingException as err:
                err_str = kctaskman.util.formatException(err)
                logger.info('task abort. actor=%s, req=%s, error=%s',
                            m.__name__, req, err_str)
                break
            except RateLimitExceeded:
                raise
            except Exception as err:
                err_str = kctaskman.util.formatException(err)
                logger.info('task exception. actor=%s, req=%s, error=%s',
                            m.__name__, req, err_str)
                retry += 1
                if retry > __cfgs['retry']:
                    break
                logger.info('retry for the %d time', retry)
                sleep(5)
                continue
            logger.info('task succ. actor=%s, req=%s, res=%s',
                        m.__name__, req, res)
            return {'actor': m.__name__, 'req': req, 'res': res}
        # end while retry
        return {'error': err_str}

    def _putcfg(key, default_value):
        actor_config[key] = __cfgs['actors'].get(key, {}).get(m.__name__, default_value)

    actor_config = {}
    _putcfg('time_limit', __cfgs['time_limit'])
    _putcfg('store_results', True)
    _putcfg('max_retries', 0)
    _putcfg('result_ttl', 24 * MS_HOUR)
    actor_config['queue_name'] = __cfgs['queue']
    actor_config['actor_name'] = m.__name__
    logger.debug('actor_config=%s', actor_config)
    return dramatiq.actor(m1, **actor_config)


def _initActors(mod):
    for k in mod.__dict__:
        if not hasattr(tasks, k):
            continue
        f = getattr(mod, k)
        if not isinstance(f, FunctionType):
            continue
        if f.__name__ == '<lambda>':
            continue
        logger.info('change function into an actor. name=%s', f.__name__)
        setattr(mod, k, _makeActor(f))


class AbortingException(Exception):
    pass


__last_broker_ns = None

__cfgs = None


def initWorker():
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])

    global __cfgs
    __cfgs = mod.configs
    global __last_broker_ns
    if not __last_broker_ns:
        __last_broker_ns = __cfgs['broker_ns']
    if __last_broker_ns != __cfgs['broker_ns']:
        raise Exception('one process can have only one broker')

    # put some default
    __cfgs.setdefault('actors', {})

    # init redis first
    broker = RedisBroker(url=__cfgs['broker'], namespace=__cfgs['broker_ns'])
    broker.add_middleware(Results(backend=RedisBackend(url=__cfgs['backend'])))
    dramatiq.set_broker(broker)

    # come after dramatiq(redis)
    _initActors(mod)

