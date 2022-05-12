import logging
from pubmed.persist.kafka_to_es_connector import KafkaToEsConnector

from pubmed.items import CiteByItem, LinkOutItem, SimilarArticleItem
from pubmed.utils.spider_utils import REMOTE_STORE_MAP
from pubmed.utils.time_utils import trace_time_elapsed
from pubmed.persist.store import EmptyStore
from pubmed.utils.spider_utils import EnviromentAwareSpider
from pubmed.persist.additional_fileds_persister import AdditionalFieldsItemsPersister

logger = logging.getLogger(__name__)


class PubmedAdditionalFiledItemPipeline:
    def __init__(self, spider: EnviromentAwareSpider, settings=None) -> None:
        self.settings = settings
        self.remote_store_cls = REMOTE_STORE_MAP.get(
            settings["REMOTE_PERTSIST_TYPE"], EmptyStore
        )
        self.connector = KafkaToEsConnector(spider.kafka_host, self.settings)
        # use EmptyStore to avoid persist additional fields in file any more, swith to FileStore if the Storage is enough.
        self.fields_persister = AdditionalFieldsItemsPersister(
            EmptyStore(self.settings), self.remote_store_cls(self.settings)
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(spider=crawler.spider, settings=crawler.settings)

    @trace_time_elapsed(logger=logger, log_level=logging.DEBUG)
    def process_item(self, item, spider):
        if isinstance(item, CiteByItem):
            file_name = item["file_name"]
            file_path = f"citedby/crawled/{file_name}.json"
            data = {"pmid": item["pmid"], "citedby_crawled": item["citedby_crawled"]}
            self.fields_persister.append(data, file_path)
            self.connector.send_message(data)
        elif isinstance(item, SimilarArticleItem):
            file_name = item["file_name"]
            file_path = f"similar_article/crawled/{file_name}.json"
            data = {
                "pmid": item["pmid"],
                "similar_articles_crawled": item["similar_articles_crawled"],
            }
            self.fields_persister.append(data, file_path)
            self.connector.send_message(data=data)
        elif isinstance(item, LinkOutItem):
            file_name = item["file_name"]
            file_path = f"linkout/crawled/{file_name}.json"
            data = {"pmid": item["pmid"], "linkout_crawled": item["linkout_crawled"]}
            self.fields_persister.append(data, file_path)
            self.connector.send_message(data)
        else:
            logger.warning(
                f"{__class__.__name__} only handle items: {CiteByItem.__name__}, {SimilarArticleItem.__name__}, {LinkOutItem.__name__}"
            )
        return item

    def close_spider(self, spider):
        self.connector.producer.flush()
        self.connector.close(timeout=500)
