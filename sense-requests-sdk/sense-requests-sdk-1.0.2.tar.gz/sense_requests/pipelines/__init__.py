from sense_requests.db import col
from sense_requests.utils import get_task_id
# from pymongo import ASCENDING
import datetime


class SenseMongoPipeline(object):
    def process_item(self, item, spider):
        item_dict = dict(item)
        item_dict['task_id'] = get_task_id()
        # col.create_index([("_ttl_time", ASCENDING)], expireAfterSeconds=3600 * 24)
        # item_dict['ttl_time'] = datetime.datetime.utcnow()
        col.save(item_dict)
        return item
