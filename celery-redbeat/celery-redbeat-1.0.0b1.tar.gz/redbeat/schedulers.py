# Licensed under the Apache License, Version 2.0 (the 'License'); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
# Copyright 2015 Marc Sibson

from __future__ import absolute_import

import calendar
import logging
import warnings
import ssl
from datetime import datetime, MINYEAR
from distutils.version import StrictVersion

try:
    import simplejson as json
except ImportError:
    import json

from celery.beat import Scheduler, ScheduleEntry, DEFAULT_MAX_INTERVAL
from celery.utils.log import get_logger
from celery.signals import beat_init
from celery.utils.time import humanize_seconds, timezone
from kombu.utils.objects import cached_property
from celery.app import app_or_default
from celery.five import values
from kombu.utils.url import maybe_sanitize_url
from tenacity import (before_sleep_log,
                      retry,
                      retry_if_exception_type,
                      stop_after_delay,
                      wait_exponential)

import redis.exceptions
from redis.client import StrictRedis
import pytz

from .decoder import (
    RedBeatJSONEncoder, RedBeatJSONDecoder,
    from_timestamp, to_timestamp
    )

# Copied from:
# https://github.com/andymccurdy/redis-py/blob/master/redis/lock.py#L33
# Changes:
#     The second line from the bottom: The original Lua script intends
#     to extend time to (lock remaining time + additional time); while
#     the script here extend time to a expected expiration time.
# KEYS[1] - lock name
# ARGS[1] - token
# ARGS[2] - additional milliseconds
# return 1 if the locks time was extended, otherwise 0
LUA_EXTEND_TO_SCRIPT = """
    local token = redis.call('get', KEYS[1])
    if not token or token ~= ARGV[1] then
        return 0
    end
    local expiration = redis.call('pttl', KEYS[1])
    if not expiration then
        expiration = 0
    end
    if expiration < 0 then
        return 0
    end
    redis.call('pexpire', KEYS[1], ARGV[2])
    return 1
"""


class RetryingConnection(object):
    """A proxy for the Redis connection that delegates all the calls to
    underlying Redis connection while retrying on connection or time-out error.
    """
    RETRY_MAX_WAIT = 30

    def __init__(self, retry_period, wrapped_connection):
        self.wrapped_connection = wrapped_connection
        self.retry_kwargs = dict(
            retry=(retry_if_exception_type(redis.exceptions.ConnectionError)
                   | retry_if_exception_type(redis.exceptions.TimeoutError)),
            reraise=True,
            wait=wait_exponential(multiplier=1, max=self.RETRY_MAX_WAIT),
            before_sleep=self._log_retry_attempt
        )
        if retry_period >= 0:
            self.retry_kwargs.update(dict(stop=stop_after_delay(retry_period)))

    def __getattr__(self, item):
        method = getattr(self.wrapped_connection, item)

        # we don't want to deal attributes or properties
        if not callable(method):
            return method

        @retry(**self.retry_kwargs)
        def retrier(*args, **kwargs):
            return method(*args, **kwargs)

        return retrier

    @staticmethod
    def _log_retry_attempt(retry_state):
        """Log when next reconnection attempt is about to be made."""
        logger.log(logging.WARNING,
                   "Retrying connection in %s seconds...",
                   retry_state.next_action.sleep)


def ensure_conf(app):
    """
    Ensure for the given app the the redbeat_conf
    attribute is set to an instance of the RedBeatConfig
    class.
    """
    name = 'redbeat_conf'
    app = app_or_default(app)
    try:
        config = getattr(app, name)
    except AttributeError:
        config = RedBeatConfig(app)
        setattr(app, name, config)

    return config


def get_redis(app=None):
    app = app_or_default(app)
    conf = ensure_conf(app)
    if not hasattr(app, 'redbeat_redis') or app.redbeat_redis is None:
        redis_options = conf.app.conf.get(
            'REDBEAT_REDIS_OPTIONS',
            conf.app.conf.get('BROKER_TRANSPORT_OPTIONS', {}))
        retry_period = redis_options.get('retry_period')
        if conf.redis_url.startswith('redis-sentinel') and  'sentinels' in redis_options:
            from redis.sentinel import Sentinel
            sentinel = Sentinel(redis_options['sentinels'],
                                socket_timeout=redis_options.get('socket_timeout'),
                                password=redis_options.get('password'),
                                db=redis_options.get('db', 0),
                                decode_responses=True)
            connection = sentinel.master_for(redis_options.get('service_name', 'master'))
        elif conf.redis_url.startswith('rediss'):
            ssl_options = { 'ssl_cert_reqs': ssl.CERT_REQUIRED }
            if isinstance(conf.redis_use_ssl, dict):
                ssl_options.update(conf.redis_use_ssl)
            connection = StrictRedis.from_url(conf.redis_url, decode_responses=True, **ssl_options)
        elif conf.redis_url.startswith('redis-cluster'):
            from rediscluster import RedisCluster
            if not redis_options.get('startup_nodes'):
                redis_options = {'startup_nodes': [{"host": "localhost", "port": "30001"}]}
            connection = RedisCluster(decode_responses=True, **redis_options)
        else:
            connection = StrictRedis.from_url(conf.redis_url, decode_responses=True)

        if retry_period is None:
            app.redbeat_redis = connection
        else:
            app.redbeat_redis = RetryingConnection(retry_period, connection)

    return app.redbeat_redis


ADD_ENTRY_ERROR = """\

Couldn't add entry %r to redis schedule: %r. Contents: %r
"""

logger = get_logger(__name__)

class RedBeatConfig(object):
    def __init__(self, app=None):
        self.app = app_or_default(app)
        self.key_prefix = self.either_or('redbeat_key_prefix', 'redbeat:')
        self.schedule_key = self.key_prefix + ':schedule'
        self.statics_key = self.key_prefix + ':statics'
        self.lock_key = self.either_or('redbeat_lock_key', self.key_prefix + ':lock')
        self.lock_timeout = self.either_or('redbeat_lock_timeout', None)
        self.redis_url = self.either_or('redbeat_redis_url', app.conf['BROKER_URL'])
        self.redis_use_ssl = self.either_or('redbeat_redis_use_ssl', app.conf['BROKER_USE_SSL'])

        self.validate_timezone()

    def validate_timezone(self):
        tz = self.app.timezone

        if tz == pytz.utc:
            return

        warnings.warn('RedBeat only supports UTC, timezone set to %s' % (tz))

    @property
    def schedule(self):
       return self.app.conf.beat_schedule

    @schedule.setter
    def schedule(self, value):
        self.app.conf.beat_schedule = value

    def either_or(self, name, default=None):
        if name == name.upper():
            warnings.warn(
                'Celery v4 installed, but detected Celery v3 '
                'configuration %s (use %s instead).' % (name, name.lower()),
                UserWarning
            )
        return self.app.conf.first(name, name.upper()) or default


class RedBeatSchedulerEntry(ScheduleEntry):
    _meta = None

    def __init__(self, name=None, task=None, schedule=None,
                 args=None, kwargs=None, enabled=True, **clsargs):
        super(RedBeatSchedulerEntry, self).__init__(name=name, task=task, schedule=schedule,
                                                    args=args, kwargs=kwargs, **clsargs)
        self.enabled = enabled
        ensure_conf(self.app)

    @staticmethod
    def load_definition(key, app=None, definition=None):
        if definition is None:
            definition = get_redis(app).hget(key, 'definition')

        if not definition:
            raise KeyError(key)

        definition = RedBeatSchedulerEntry.decode_definition(definition)

        return definition

    @staticmethod
    def decode_definition(definition):
        return json.loads(definition, cls=RedBeatJSONDecoder)

    @staticmethod
    def load_meta(key, app=None):
        return RedBeatSchedulerEntry.decode_meta(get_redis(app).hget(key, 'meta'))

    @staticmethod
    def decode_meta(meta, app=None):
        if not meta:
            return {'last_run_at': None}

        return json.loads(meta, cls=RedBeatJSONDecoder)

    @classmethod
    def from_key(cls, key, app=None):
        ensure_conf(app)
        with get_redis(app).pipeline() as pipe:
            pipe.hget(key, 'definition')
            pipe.hget(key, 'meta')
            definition, meta = pipe.execute()

        if not definition:
            raise KeyError(key)

        definition = cls.decode_definition(definition)
        meta = cls.decode_meta(meta)
        definition.update(meta)

        entry = cls(app=app, **definition)
        # celery.ScheduleEntry sets last_run_at = utcnow(), which is confusing and wrong
        entry.last_run_at = meta['last_run_at']

        return entry

    @property
    def due_at(self):
        # never run => due now
        if self.last_run_at is None:
            return self._default_now()

        delta = self.schedule.remaining_estimate(self.last_run_at)
        # if no delta, means no more events after the last_run_at.
        if delta is None:
            return None

        # overdue => due now
        if delta.total_seconds() < 0:
            return self._default_now()

        return self.last_run_at + delta

    @property
    def key(self):
        return self.app.redbeat_conf.key_prefix + self.name

    @property
    def score(self):
        if self.due_at is None:
            # Scores < zero are ignored on each tick.
            return -1
        return to_timestamp(self.due_at)

    @property
    def rank(self):
        return get_redis(self.app).zrank(self.app.redbeat_conf.schedule_key, self.key)

    def save(self):
        definition = {
            'name': self.name,
            'task': self.task,
            'args': self.args,
            'kwargs': self.kwargs,
            'options': self.options,
            'schedule': self.schedule,
            'enabled': self.enabled,
        }
        meta = {
            'last_run_at': self.last_run_at,
        }
        with get_redis(self.app).pipeline() as pipe:
            pipe.hset(self.key, 'definition', json.dumps(definition, cls=RedBeatJSONEncoder))
            pipe.hsetnx(self.key, 'meta', json.dumps(meta, cls=RedBeatJSONEncoder))
            pipe.zadd(self.app.redbeat_conf.schedule_key, {self.key: self.score})
            pipe.execute()

        return self

    def delete(self):
        with get_redis(self.app).pipeline() as pipe:
            pipe.zrem(self.app.redbeat_conf.schedule_key, self.key)
            pipe.delete(self.key)
            pipe.execute()

    def _next_instance(self, last_run_at=None, only_update_last_run_at=False):
        entry = super(RedBeatSchedulerEntry, self)._next_instance(last_run_at=last_run_at)

        if only_update_last_run_at:
            # rollback the update to total_run_count
            entry.total_run_count = self.total_run_count

        meta = {
            'last_run_at': entry.last_run_at,
            'total_run_count': entry.total_run_count,
        }

        with get_redis(self.app).pipeline() as pipe:
            pipe.hset(self.key, 'meta', json.dumps(meta, cls=RedBeatJSONEncoder))
            pipe.zadd(self.app.redbeat_conf.schedule_key, {entry.key: entry.score})
            pipe.execute()

        return entry
    __next__ = next = _next_instance

    def reschedule(self, last_run_at=None):
        self.last_run_at = last_run_at or self._default_now()
        meta = {
            'last_run_at': self.last_run_at,
        }
        with get_redis(self.app).pipeline() as pipe:
            pipe.hset(self.key, 'meta', json.dumps(meta, cls=RedBeatJSONEncoder))
            pipe.zadd(self.app.redbeat_conf.schedule_key, {self.key: self.score})
            pipe.execute()

    def is_due(self):
        if not self.enabled:
            return False, 5.0  # 5 second delay for re-enable.

        return self.schedule.is_due(self.last_run_at or datetime(MINYEAR, 1, 2, tzinfo=self.schedule.tz))


class RedBeatScheduler(Scheduler):
    # how often should we sync in schedule information
    # from the backend redis database
    Entry = RedBeatSchedulerEntry

    lock = None

    #: The default lock timeout in seconds.
    lock_timeout = DEFAULT_MAX_INTERVAL * 5

    def __init__(self, app, lock_key=None, lock_timeout=None, **kwargs):
        ensure_conf(app)  # set app.redbeat_conf
        self.lock_key = lock_key or app.redbeat_conf.lock_key
        self.lock_timeout = (lock_timeout or
                             app.redbeat_conf.lock_timeout or
                             self.max_interval * 5 or
                             self.lock_timeout)
        super(RedBeatScheduler, self).__init__(app, **kwargs)

    def setup_schedule(self):
        # cleanup old static schedule entries
        client = get_redis(self.app)
        previous = set(key for key in client.smembers(self.app.redbeat_conf.statics_key))
        removed = previous.difference(self.app.redbeat_conf.schedule.keys())

        for name in removed:
            logger.debug("Removing old static schedule entry '%s'.", name)
            with client.pipeline() as pipe:
                RedBeatSchedulerEntry(name, app=self.app).delete()
                pipe.srem(self.app.redbeat_conf.statics_key, name)
                pipe.execute()

        # setup static schedule entries
        self.install_default_entries(self.app.redbeat_conf.schedule)
        if self.app.redbeat_conf.schedule:
            self.update_from_dict(self.app.redbeat_conf.schedule)

            # keep track of static schedule entries,
            # so we notice when any are removed at next startup
            client.sadd(self.app.redbeat_conf.statics_key,
                        *self.app.redbeat_conf.schedule.keys())

    def update_from_dict(self, dict_):
        for name, entry in dict_.items():
            try:
                entry = self._maybe_entry(name, entry)
            except Exception as exc:
                logger.error(ADD_ENTRY_ERROR, name, exc, entry)
                continue

            entry.save()  # store into redis
            logger.debug("Stored entry: %s", entry)

    def reserve(self, entry):
        new_entry = next(entry)
        return new_entry

    @property
    def schedule(self):
        logger.debug('Selecting tasks')

        max_due_at = to_timestamp(self.app.now())
        client = get_redis(self.app)

        with client.pipeline() as pipe:
            pipe.zrangebyscore(self.app.redbeat_conf.schedule_key, 0, max_due_at)

            # peek into the next tick to accuratly calculate sleep between ticks
            pipe.zrangebyscore(self.app.redbeat_conf.schedule_key,
                               '({}'.format(max_due_at),
                               max_due_at + self.max_interval,
                               start=0, num=1)
            due_tasks, maybe_due = pipe.execute()

        logger.info('Loading %d tasks', len(due_tasks) + len(maybe_due))
        d = {}
        for key in due_tasks + maybe_due:
            try:
                entry = self.Entry.from_key(key, app=self.app)
            except KeyError:
                logger.warning('failed to load %s, removing', key)
                client.zrem(self.app.redbeat_conf.schedule_key, key)
                continue

            d[entry.name] = entry

        return d

    def maybe_due(self, entry, **kwargs):
        is_due, next_time_to_run = entry.is_due()

        if is_due:
            logger.info('Scheduler: Sending due task %s (%s)', entry.name, entry.task)
            try:
                result = self.apply_async(entry, **kwargs)
            except Exception as exc:
                logger.exception('Message Error: %s', exc)
            else:
                logger.debug('%s sent. id->%s', entry.task, result.id)
        return next_time_to_run

    def tick(self, min=min, **kwargs):
        if self.lock:
            logger.debug('beat: Extending lock...')
            self.lock.extend(int(self.lock_timeout))

        remaining_times = []
        try:
            for entry in values(self.schedule):
                next_time_to_run = self.maybe_due(entry, **self._maybe_due_kwargs)
                if next_time_to_run:
                    remaining_times.append(next_time_to_run)
        except RuntimeError:
            logger.debug('beat: RuntimeError', exc_info=True)

        return min(remaining_times + [self.max_interval])

    def close(self):
        if self.lock:
            logger.debug('beat: Releasing Lock')
            self.lock.release()
            self.lock = None
        super(RedBeatScheduler, self).close()

    @property
    def info(self):
        info = ['       . redis -> {}'.format(maybe_sanitize_url(self.app.redbeat_conf.redis_url))]
        if self.lock_key:
            info.append('       . lock -> `{}` {} ({}s)'.format(
                self.lock_key, humanize_seconds(self.lock_timeout), self.lock_timeout))
        return '\n'.join(info)

    @cached_property
    def _maybe_due_kwargs(self):
        """ handle rename of publisher to producer """
        return {'producer': self.producer}

@beat_init.connect
def acquire_distributed_beat_lock(sender=None, **kwargs):
    scheduler = sender.scheduler
    if not scheduler.lock_key:
        return

    logger.debug('beat: Acquiring lock...')
    redis_client = get_redis(scheduler.app)

    lock = redis_client.lock(
        scheduler.lock_key,
        timeout=scheduler.lock_timeout,
        sleep=scheduler.max_interval,
    )
    # overwrite redis-py's extend script
    # which will add additional timeout instead of extend to a new timeout
    lock.lua_extend = redis_client.register_script(LUA_EXTEND_TO_SCRIPT)
    lock.acquire()

    scheduler.lock = lock
