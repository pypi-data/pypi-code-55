from redisbloom.client import Client
from redis.exceptions import ResponseError
import logging
import os

logger = logging.getLogger('filter')
logger.setLevel(logging.INFO)

HOST = os.environ.get('BLOOM_FILTER_HOST', None)
PORT = int(os.environ.get('BLOOM_FILTER_PORT', '36379'))
filter_name = 'bloom'

filter = None
if HOST:
    filter = Client(host=HOST, port=PORT)
    logger.info('connect filter success')
else:
    logger.info('not found bloom filter env, skip init filter')

if filter:
    try:
        filter.bfCreate(filter_name, 0.0001, 1000000000)
    except ResponseError as e:
        if e.args[0] != 'item exists':
            raise e
        logger.info(f'filter exists {filter_name}')
else:
    logger.info('not found filter, sikp init filter')


def build_filter_data(spider_name, unique_id):
    return spider_name + unique_id


# check data for existence
def check(spider_name, unique_id):
    return filter.bfExists(
        filter_name, build_filter_data(spider_name, unique_id))


# save data to filter
def save(spider_name, unique_id):
    filter.bfAdd(filter_name, build_filter_data(spider_name, unique_id))
