from collections import Set
from time import sleep

import dramatiq
from dramatiq import RateLimitExceeded, Worker

from conf import conf
from lib import util
from lib.util import AbortingException, MS_HOUR
from taskmanager.log import logger


def addActor(x, m, **kwargs):
    def m1(*req, **kwargs):
        logger.info('task start. actor=%s, req=%s',
                    m.__name__, req)
        retry = 0
        while True:
            try:
                res = m(*req)
            except AbortingException as err:
                err_str = util.formatException(err)
                logger.info('task abort. actor=%s, req=%s, error=%s',
                            m.__name__, req, err_str)
                break
            except RateLimitExceeded:
                raise
            except Exception as err:
                err_str = util.formatException(err)
                logger.info('task exception. actor=%s, req=%s, error=%s',
                            m.__name__, req, err_str)
                retry += 1
                if retry > conf.worker.retry:
                    break
                logger.info('retry for the %d time', retry)
                sleep(5)
                continue
            logger.info('task succ. actor=%s, req=%s, ret=%s',
                        m.__name__, req, res)
            return {'actor': m.__name__, 'req': req, 'res': res}
        # end while retry
        return {'error': err_str}

    kwargs.setdefault('time_limit', conf.full.task_timeout)
    kwargs.setdefault('store_results', True)
    kwargs.setdefault('max_retries', 0)
    kwargs.setdefault('result_ttl', 10 * 24 * MS_HOUR)
    kwargs.setdefault('queue_name', x.name)
    kwargs['actor_name'] = m.__name__
    setattr(x, m.__name__, dramatiq.actor(m1, **kwargs))


