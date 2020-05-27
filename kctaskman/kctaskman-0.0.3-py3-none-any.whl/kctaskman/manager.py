import json
import time
import traceback
from time import sleep

import dramatiq
from dramatiq import Actor, pipeline
from dramatiq.results import ResultMissing

import kctaskman.util
from kctaskman.scaler import Scaler
from kctaskman.log import logger
from storage import Storage
import schedule as schedulelib


class ActorError(Exception):
    pass


class Manager:
    def __init__(self, worker, cfgs):
        self._cfgs = cfgs
        self._queue = worker.configs['queue']
        self._worker = worker
        logger.info('create contoller, queue=%s', self._queue)
        self._store = Storage(cfgs['type'])
        self._type = cfgs['type']
        self._taskinfos = {}
        self._scaler = Scaler(
            cfgs['kubernetes_api'],
            "Bearer AKK63ZZCVJ4F32RMB6",
            f'{cfgs["app"]}-{self._queue}')

    def scale(self, n):
        self._scaler.scale(n)

    def __cleanAll(self):
        logger.info('cleanAll for queue=%s', self._queue)
        if self._cfgs.get('reset_worker', True):
            self.scale(0)
        dramatiq.get_broker().flush_all()

    def __enter__(self):
        self.__cleanAll()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('controller exit. queue=%s, err_type=%s, err_val=%s',
                    self._queue, exc_type, exc_val)
        traceback.print_tb(exc_tb)
        self.__cleanAll()

    @staticmethod
    def descActorInfos(actorinfos, common_args):
        desc = []
        for x in actorinfos:
            if isinstance(x, list):
                actor, actor_args = x
            else:
                actor = x
                actor_args = None
            s = actor.actor_name
            if actor_args:
                s += '('
                s += json.dumps(actor_args)
                s += ')'
            desc.append(s)
        desc.append('common_args=' + json.dumps(common_args))
        return '+'.join(desc)

    def startPipeline(self, *actorinfos, prepend_args=[], append_args=[]):
        p: pipeline = None
        for x in actorinfos:
            if isinstance(x, list):
                actor = x[0]
                actor_args = x[1:]
            else:
                actor = x
                actor_args = []
            msg = actor.message(
                *prepend_args,
                *actor_args,
                *append_args,
                queue_name=self._queue)
            if p:
                p = p | msg
            else:
                p = msg
        taskmsg = p.run()
        desc = Manager.descActorInfos(actorinfos, prepend_args)
        self._taskinfos.setdefault(desc, [])
        self._taskinfos[desc].append({
            'req': {
                'type': 'pipeline',
                'prepend_args': prepend_args,
                'append_args': append_args,
            },
            'taskmsg': taskmsg,
            'noticed': True,
            'name': desc,
        })
        logger.debug('issue pipeline. desc=%s,', desc)

    def start(self, actor, *req):
        logger.debug('issue task. req=%s', req)
        if isinstance(actor, Actor):
            taskmsg = actor.send(*req, queue_name=self._queue)
        else:
            raise NotImplementedError()
        self._taskinfos.setdefault(actor.actor_name, [])
        self._taskinfos[actor.actor_name].append({
            'req': req,
            'taskmsg': taskmsg,
            'noticed': True,
            'name': actor.actor_name,
        })
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

    def awaitAll(self, timeout=None):
        timeout = timeout or self._cfgs['await_timeout']
        t0 = kctaskman.util.nowms()
        last_completed_count = -1
        while True:
            t1 = kctaskman.util.nowms()
            if t1 - t0 > timeout:
                raise Exception('waitAll timeout')

            self.fetchNewResults()
            total = self.getTotal()
            completed_count = self.getCompletedCount()
            for t in filter(lambda x: not x['noticed'], self.getAllTaskInfos()):
                logger.info('one task completed. total=%d, remain=%d, actor=%s, req=%s, res=%s',
                            total,
                            total - completed_count,
                            t['name'],
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
                if r and 'error' in r:
                    logger.error('task error. result=%s', r)
                    raise ActorError()
                taskinfo['noticed'] = False
                taskinfo['res'] = r['res']
            except ResultMissing:
                continue

    def getCompletedCount(self):
        return len(list(filter(lambda x: 'res' in x, self.getAllTaskInfos())))

    def runWithTypePartitions(self, actor: Actor, *req1, partitions=None, timeout=None, type=None):
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


class Schedule:
    PLANS_KEY = 'full_schedules'

    def __init__(self):
        self._global_store = Storage('global')

    def main(self):
        raise NotImplementedError

    @staticmethod
    def _job(self, args):
        try:
            self.main(args)
            logger.info('job success.')
        except Exception as err:
            logger.error(kctaskman.util.formatException(err))

    def reschedule(self, plans):
        # db.xxx_global.update({_id: 'full_schedules'}, {value: ['01:01']}, {upsert: true})
        self._global_store.saveVar(self.PLANS_KEY, plans)

    def runForever(self, args):

        last_schedules = []
        while True:
            schedules = self._global_store.loadVarOrSave(self.PLANS_KEY, [])
            if schedules is None or len(schedules) == 0:
                logger.info('no schedules found, please insert config. config_key=%s', self.PLANS_KEY)
                time.sleep(5)
                continue
            if ','.join(last_schedules) != ','.join(schedules):
                logger.info('start updating schedules: %s', schedules)
                schedulelib.clear()
                for schedule in schedules:
                    try:
                        schedulelib.every().day.at(schedule).do(self._job, self, args)
                    except Exception as err:
                        logger.error('fail to parse schedule: %s', schedule)
                        logger.error(err)
                last_schedules = schedules
                logger.info('finish updating schedules: %s', schedules)
            if schedulelib.idle_seconds() <= 0:
                schedulelib.run_pending()
            else:
                time.sleep(15)
