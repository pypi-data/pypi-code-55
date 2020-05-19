from loguru import logger
import redis

# from __init__ import __version__


class Locli:
    def __init__(
        self,
        key=None,
        handler=None,
        host='localhost',
        port=6379,
        db=1,
    ):
        self._redis = redis.Redis(host=host, port=port, db=db)

        if None in (key, handler):
            logger.debug({
                'setting': 'key or handler is None!',
            })
            return

        self._user_handler = handler
        pubsub = self._redis.pubsub(ignore_subscribe_messages=True)
        pkey = key + '*'
        pubsub.psubscribe(**{pkey: self._user_handler})
        pubsub.run_in_thread(sleep_time=0.001)

        self._get_to_pub(key, pkey)

    def _get_to_pub(self, key, pkey):
        data = self._redis.hgetall(key)
        if data is None:
            return

        for k, v in data.items():
            message = {
                'type': 'init',
                'pattern': pkey.encode(),
                'channel': (key + '/' + k.decode()).encode(),
                'data': v,
            }
            self._user_handler(message)

    def put(self, key, field, value):
        with self._redis.pipeline() as p:
            p.hset(key, field, value)
            p.publish(key + '/' + field, str(value))
            p.execute()
