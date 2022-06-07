import logging

from pubmed.items import PubmedArticleSetItem
from pubmed.utils.spider_utils import REMOTE_STORE_MAP
from pubmed.utils.time_utils import trace_time_elapsed
from pubmed.persist.store import EmptyStore, FileStore

from pubmed.persist.additional_fileds_persister import AdditionalFieldsPersister

logger = logging.getLogger(__name__)


class PubmedAdditionalFiledPipeline:
    def __init__(self, settings=None) -> None:
        self.settings = settings
        self.remote_store_cls = REMOTE_STORE_MAP.get(
            settings["REMOTE_PERTSIST_TYPE"], EmptyStore
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    @trace_time_elapsed(logger=logger)
    def process_item(self, item, spider):
        if isinstance(item, PubmedArticleSetItem):
            persister = AdditionalFieldsPersister(
                FileStore(self.settings), self.remote_store_cls(self.settings)
            )
            result_paths = persister.save(dict(item))
            item["citedby_crawled_path"] = result_paths["citedby_crawled_path"]
            item["simlar_article_crawled_path"] = result_paths[
                "simlar_article_crawled_path"
            ]
            item["linkout_path"] = result_paths["linkout_path"]
            return item
        else:
            logger.warning(
                f"{__class__.__name__} only handle item: {PubmedArticleSetItem.__name__}"
            )
