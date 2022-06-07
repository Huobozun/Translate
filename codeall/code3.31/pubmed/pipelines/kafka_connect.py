import logging
from pubmed.utils.spider_utils import EnviromentAwareSpider
from pubmed.persist.kafka_to_es_connector import KafkaToEsConnector
from pubmed.items import PubmedArticleSetItem
from pubmed.utils.time_utils import trace_time_elapsed

logger = logging.getLogger(__name__)


class PubmedKafkaPipeline:
    def __init__(self, spider: EnviromentAwareSpider, settings=None) -> None:
        self.settings = settings
        self.connector = KafkaToEsConnector(spider.kafka_host, self.settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(spider=crawler.spider, settings=crawler.settings)

    @trace_time_elapsed(logger=logger)
    def process_item(self, item, spider):
        if isinstance(item, PubmedArticleSetItem):
            if "article_path" in item and item["article_path"]:
                # create or update record
                self.connector.send_message_from_file(item["article_path"])
            if "deletion_path" in item and item["deletion_path"]:
                # only update deleted field
                self.connector.send_message_from_file(item["deletion_path"])
            if "citedby_crawled_path" in item and item["citedby_crawled_path"]:
                # only update citedby_crawled field
                self.connector.send_message_from_file(item["citedby_crawled_path"])
            if "simlar_article_crawled_path" in item and item["simlar_article_crawled_path"]:
                # only update simlar_article_crawled field
                self.connector.send_message_from_file(
                    item["simlar_article_crawled_path"]
                )
            if "linkout_path" in item and item["linkout_path"]:
                # only update simlar_article_crawled field
                self.connector.send_message_from_file(item["linkout_path"])
            return item
