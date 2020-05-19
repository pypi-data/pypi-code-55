from scrapy.exceptions import DropItem
import datetime


class ItemCheckPipeline(object):

    def process_item(self, item, spider):
        unique_id = item.get('unique_id')
        if not unique_id:
            spider.logger.error(f'unique_id is None')
            raise DropItem('unique_id is None')

        queues = item.queue_names()
        if len(queues) == 0:
            spider.logger.warn(f'queue_names length is 0')
        item['crawled_at'] = datetime.datetime.utcnow().replace(
                        tzinfo=datetime.timezone.utc).astimezone().isoformat()

        oss_filename = item.get('oss_filename')
        if not oss_filename:
            if unique_id.find('/') != -1:
                msg = 'unique_id format error, find / in unicode_id'
                spider.logger.error(msg)
                raise DropItem(msg)
            oss_filename = f'{spider.name}/{unique_id}'
            item['oss_filename'] = oss_filename
        return item
