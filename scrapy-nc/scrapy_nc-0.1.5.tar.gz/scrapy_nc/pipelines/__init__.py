from .amqp_pipeline import AMQPPipeline
from .oss_pipeline import OSSPipeline
from .mongo_pipeline import MongoPipeline
from .item_check_pipeline import ItemCheckPipeline
from .filter_pipeline import FilterCheckPipeline, FilterSavePipeline
from .request import RequestPipeline

# from .redis_duplicate_pipeline import RedisDuplicatesPipeline

ITEM_CHECK_PIPELINE = 'scrapy_nc.pipelines.ItemCheckPipeline'
FILTER_CHECK_PIPELINE = 'scrapy_nc.pipelines.FilterCheckPipeline'
OSS_PIPELINE = 'scrapy_nc.pipelines.OSSPipeline'
AMQP_PIPELINE = 'scrapy_nc.pipelines.AMQPPipeline'
MONGO_PIPELINE = 'scrapy_nc.pipelines.MongoPipeline'
FILTER_SAVE_PIPELINE = 'scrapy_nc.pipelines.FilterSavePipeline'
REQUEST_PIPELINE = 'scrapy_nc.pipelines.RequestPipeline'

DEFAULT_PIPELINES = {
    ITEM_CHECK_PIPELINE: 500,
    FILTER_CHECK_PIPELINE: 550,
    OSS_PIPELINE: 600,
    AMQP_PIPELINE: 650,
    MONGO_PIPELINE: 700,
    FILTER_SAVE_PIPELINE: 750,
    REQUEST_PIPELINE: 760,
}
