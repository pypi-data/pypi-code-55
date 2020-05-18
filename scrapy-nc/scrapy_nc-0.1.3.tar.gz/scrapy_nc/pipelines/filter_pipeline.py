from scrapy_nc.filter import filter, build_filter_data
from scrapy_nc.filter import filter_name
from scrapy.exceptions import DropItem


class FilterSavePipeline(object):

    def process_item(self, item, spider):
        unique_id = item.get('unique_id')
        filter.bfAdd(filter_name, build_filter_data(spider.name, unique_id))
        spider.logger.info(f'save to filter {unique_id} {spider.name}')
        return item


class FilterCheckPipeline(object):
    def process_item(self, item, spider):
        unique_id = item.get('unique_id')
        if filter.bfExists(filter_name, build_filter_data(spider.name, unique_id)):
            raise DropItem(f"exists item {spider.name} {item['unique_id']}")
        return item
