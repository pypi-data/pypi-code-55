import time
import traceback
from time import sleep

import dramatiq
from dramatiq import Actor, pipeline
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import ResultMissing, Results
from dramatiq.results.backends import RedisBackend

from conf import conf
from lib import util
from taskmanager.log import logger
from storage import Storage
from taskmanager import scale


class ActorError(Exception):
    pass


class Controller:
    def __init__(self, worker, type):
        self._worker = worker
        logger.info('create contoller, name=%s', worker.__name__)
        self._store = Storage(type)
        self._type = type
        self._taskinfos = {}


    def scale(self, n):
        scale.scale(self._worker.__name__, n)

    def __cleanAll(self):
        logger.info('cleanAll for worker=%s', self._worker.__name__)
        self.scale(0)
        dramatiq.get_broker().flush_all()

    def __enter__(self):
        self.__cleanAll()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('controller exit. worker=%s, err_type=%s, err_val=%s',
                    self._worker.__name__, exc_type, exc_val)
        traceback.print_tb(exc_tb)
        self.__cleanAll()

    def start(self, actor, *req):
        actor: Actor
        taskmsg = actor.send(*req, queue_name=self._worker.__name__)
        t = {'req': req, 'taskmsg': taskmsg, 'noticed': True, }
        self._taskinfos.setdefault(actor.actor_name, [])
        self._taskinfos[actor.actor_name].append(t)
        logger.info('task issued. all=%s, req=%s', self.getSummary(), req)

    def getAllTaskInfos(self):
        s = []
        for k, v in self._taskinfos.items():
            s += v
        return s

    def getSummary(self):
        s = []
        for k, v in self._taskinfos.items():
            s.append(f'{k}({len(v)})')
        return ' '.join(s)

    def getTotal(self):
        s = 0
        for k, v in self._taskinfos.items():
            s += len(v)
        return s

    def awaitAll(self, timeout=conf.full.step_timeout):
        t0 = util.nowts()
        last_completed_count = -1
        while True:
            t1 = util.nowts()
            if t1 - t0 > timeout:
                raise Exception('waitAll timeout')

            self.fetchNewResults()
            total = self.getTotal()
            completed_count = self.getCompletedCount()
            for t in filter(lambda x: not x['noticed'], self.getAllTaskInfos()):
                logger.info('one task completed. total=%d, remain=%d, actor=%s, req=%s, res=%s',
                            total,
                            total - completed_count,
                            t['taskmsg'].actor_name,
                            t['req'],
                            t['res'])
                t['noticed'] = True
            if last_completed_count != completed_count:
                # some task finishes or this is the first time
                last_completed_count = completed_count

            if last_completed_count == self.getTotal():
                break
            sleep(1)
        results = list(map(lambda x: x['res'], self.getAllTaskInfos()))
        self._taskinfos = {}
        return results

    def fetchNewResults(self):
        for taskinfo in self.getAllTaskInfos():
            if 'res' in taskinfo:
                continue
            try:
                r = taskinfo['taskmsg'].get_result()
                taskinfo['noticed'] = False
                taskinfo['res'] = r['res']
                assert r['actor'] == taskinfo['taskmsg'].actor_name
                if r and 'error' in r:
                    logger.error('task error. taskinfo=%s', taskinfo)
                    raise ActorError()
            except ResultMissing:
                continue

    def getCompletedCount(self):
        return len(list(filter(lambda x: 'res' in x, self.getAllTaskInfos())))

    def run(self, actor: Actor, partitions=None, *req1, timeout=conf.full.step_timeout, type=None):
        if not type:
            type = self._type
        logger.info('step start. actor=%s, partitions=%s', actor.actor_name, partitions)
        if hasattr(partitions, '__iter__'):
            PARTITIONS = len(partitions)
            if PARTITIONS == 0:
                return
            for partition in partitions:
                self.start(actor, type, partition, PARTITIONS, *req1)

        else:
            self.start(actor, type, *req1)
        results = self.awaitAll(timeout=timeout)
        logger.info('step finish. actor=%s', actor.actor_name)
        if partitions and hasattr(partitions, '__iter__'):
            return results
        else:
            return results[0]


def waitPipeline(pinfos):
    finish = 0
    last_print_at_len = -1
    while len(pinfos) > 0:
        done = 0
        for i in range(len(pinfos)):
            p: pipeline = pinfos[i][1]
            if p.completed:
                r = p.get_result(block=True)
                done += 1
                logger.info('pipeline finish. pid=%d, finish=%d, remain=%d, ret=%s',
                            pinfos[i][0], finish, len(pinfos) - done, r)
                pinfos[i] = None
        if done > 0:
            finish += done
            pinfos = list(filter(lambda x: x, pinfos))
        else:
            time.sleep(1)
        if len(pinfos) < 10 and last_print_at_len != len(pinfos):
            logger.info('remain=%s', pinfos)
            last_print_at_len = len(pinfos)


__last_main = None
def initBroker(broker_ns):
    global __last_main
    if not __last_main:
        __last_main = broker_ns
    if __last_main != broker_ns:
        raise Exception('one controller must have workers of same broker')
    broker = RedisBroker(url=conf.distq.broker, namespace=conf.distq.broker_namespace_prefix + broker_ns)
    broker.add_middleware(Results(backend=RedisBackend(url=conf.distq.backend)))
    dramatiq.set_broker(broker)
    return broker