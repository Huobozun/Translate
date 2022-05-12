import logging

from pubmed.items import PubmedArticleSetItem
from pubmed.utils.time_utils import trace_time_elapsed
from pubmed.utils.spider_utils import EnviromentAwareSpider
from pubmed.persist.spider_status_connector import KafkaSpiderStatusConnector


logger = logging.getLogger(__name__)


class PubmedSavePageCrawledStatusPipeline:
    def __init__(self, spider: EnviromentAwareSpider, settings=None) -> None:
        self.settings = settings
        self.spilder_status_connector = KafkaSpiderStatusConnector(
            spider.kafka_host, self.settings
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(spider=crawler.spider, settings=crawler.settings)

    @trace_time_elapsed(logger=logger)
    def process_item(self, item, spider):
        if isinstance(item, PubmedArticleSetItem):
            self.spilder_status_connector.add_crawled_page(item)
            return item
