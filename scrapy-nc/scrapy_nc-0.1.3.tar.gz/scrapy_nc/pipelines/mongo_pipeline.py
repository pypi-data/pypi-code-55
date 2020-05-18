from scrapy_nc.crawlab import get_task_id
from scrapy_nc.db import mongo_db
import json


class MongoPipeline(object):
    def process_item(self, item, spider):
        if not self.spider_collection:
            spider.logger.warn(f'mongodb not collected, ignore save')
            return item
        ensure_unique_index = spider.settings.get('ENSURE_UNIQUE_INDEX')
        my_item = item.deepcopy()
        if my_item.get('html'):
            my_item['html'] = None
        item_dict = dict(my_item)
        item_dict['task_id'] = get_task_id()
        if ensure_unique_index:
            self.spider_collection.update_one({
                'unique_id':   my_item.get('unique_id')
            }, {"$set": item_dict}, upsert=True)
        else:
            self.spider_collection.update_one({
                'unique_id':   my_item.get('unique_id'),
                'task_id':   my_item.get('task_id')
            }, {"$set": item_dict}, upsert=True)
        return item

    def open_spider(self, spider):
        spider.logger.info('open_spider')
        if not mongo_db:
            self.spider_collection = None
            spider.logger.error('mongodb not configed')
            return

        self.spider_collection = mongo_db.get_collection(spider.name)
        ensure_unique_index = spider.settings.get('ENSURE_UNIQUE_INDEX')

        res = json.dumps(self.spider_collection.index_information())
        spider.logger.info(
            f'index_information {res}')
        if ensure_unique_index:
            index_name = 'unique_id'
            if index_name not in self.spider_collection.index_information():
                self.spider_collection.create_index(
                    'unique_id', unique=True, name=index_name)
        else:
            index_name = 'unique_id_task_id'
            if index_name not in self.spider_collection.index_information():
                self.spider_collection.create_index(
                    [('unique_id', 1), ('task_id', 1)], unique=True, name=index_name)