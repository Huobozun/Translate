import os
import logging
from pubmed.items import PubmedArticleSetItem
from pubmed.utils.time_utils import trace_time_elapsed
from pubmed.utils.spider_utils import EnviromentAwareSpider

logger = logging.getLogger(__name__)


class CleanLocalFilePipeline:
    def __init__(self, settings=None) -> None:
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    @trace_time_elapsed(logger=logger)
    def process_item(self, item, spider: EnviromentAwareSpider):
        if isinstance(item, PubmedArticleSetItem):
            if "article_path" in item and item["article_path"]:
                # only clean article json files, other files are still needed.
                os.remove(item["article_path"])
            return item
