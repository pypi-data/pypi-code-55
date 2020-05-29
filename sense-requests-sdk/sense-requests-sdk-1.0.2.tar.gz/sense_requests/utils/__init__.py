import os
from pymongo import ASCENDING
import datetime


def get_task_id():
    return os.environ.get('SENSE_TASK_ID')


def save_item(item):
    from sense_requests.db import col
    col.create_index([("_ttl_time", ASCENDING)], expireAfterSeconds=3600 * 24)
    item['ttl_time'] = datetime.datetime.utcnow()
    item['task_id'] = get_task_id()
    col.save(item)


