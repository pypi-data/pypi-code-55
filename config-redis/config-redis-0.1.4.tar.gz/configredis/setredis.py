import redis
import logging
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SetRedis:
    def __init__(self):
        self.__obj = redis.StrictRedis(**SetRedis.connetion())

    @staticmethod
    def connetion(conf_redis: dict = None):
        """
        get redis config form your environ or enter.
        redis config name use >CONF_FOR_REDISCONF<
        :param conf_redis: redis config args.
        :return: dict of redis config
        """
        try:
            redis_conf = conf_redis or eval(os.environ['CONF_FOR_REDISCONF'])
        except KeyError:
            os.environ['CONF_FOR_REDISCONF'] = input(
                "WARNING:\n Haven't catch redis config from your env.\n Entry CONF_FOR_REDISCONF args：")
            redis_conf = eval(os.environ['CONF_FOR_REDISCONF'])
        return redis_conf

    @staticmethod
    def getkeys():
        """
        get all fields from redis.
        :return: get fields(keys) list
        """
        return SetRedis().__obj.keys()

    @staticmethod
    def getfiels(name):
        """
        get value according fields.
        :param name: redis fields
        :return: get keys and values according fields.
        """
        try:
            return SetRedis().__obj.hgetall(name)
        except redis.exceptions.ResponseError:
            return SetRedis().__obj.get(name)

    @staticmethod
    def upsert(name, mapping=None, **kwargs):
        """
        create or update mapping according fields.
        :param name: redis key
        :param mapping: <dict> data what is create or update
        """
        mapping = {**mapping, **kwargs} if mapping else kwargs
        mapping = {k: json.dumps(v) for k, v in mapping.items()}
        SetRedis().__obj.hmset(name, mapping)
        logger.info(f"→{name}← has been setup the mapping: →{mapping}← done.")

    @staticmethod
    def delfiels(name, *keys):
        """
        delete concent from name or key.
        :param name: redis fields
        :param keys: redis fields keys
        :return: notice
        """
        if keys:
            SetRedis().__obj.hdel(name, *keys)
            logger.info(f"→{name}← has been delete →{keys}←.")
        else:
            SetRedis().__obj.delete(name)
            logger.info(f"→{name}← and mapping delete already.")
