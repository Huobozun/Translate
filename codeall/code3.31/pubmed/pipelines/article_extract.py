import os
import logging
from pubmed.items import FileDownloadedResultItem, PubmedArticleSetItem
from pubmed.utils.spider_utils import REMOTE_STORE_MAP
from pubmed.utils.time_utils import trace_time_elapsed
from pubmed.persist.store import EmptyStore, FileStore

from pubmed.persist.pubmed_xml_persister import PubmedXmlPersister
from pubmed.parser.pubmed_xml_parser import PubmedXmlParser

logger = logging.getLogger(__name__)


class PubmedArticleExtractPipeline:
    def __init__(self, settings=None):
        self.settings = settings
        self.download_store_uri = settings["FILES_STORE"]
        self.remote_store_cls = REMOTE_STORE_MAP.get(
            settings["REMOTE_PERTSIST_TYPE"], EmptyStore
        )
        self.example_pmids = settings.get("EXAMPLE_PMIDS", [])

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    @trace_time_elapsed(logger=logger)
    def process_item(self, item, spider):
        if isinstance(item, FileDownloadedResultItem):
            result_path = os.path.join(self.download_store_uri, item["path"])
            dict_out = PubmedXmlParser.parse_pubmed_xml_gz(result_path)
            persister = PubmedXmlPersister(
                FileStore(self.settings),
                self.remote_store_cls(self.settings),
                self.example_pmids,
            )
            result_paths = persister.save(dict_out)
            result_item = PubmedArticleSetItem()
            result_item["file_url"] = item["url"]
            result_item["file_name"] = item["path"]
            result_item["file_path"] = result_path
            result_item["deletion_path"] = result_paths["deletion_path"]
            result_item["article_id_path"] = result_paths["article_id_path"]
            result_item["article_path"] = result_paths["article_path"]
            result_item["reference_path"] = result_paths["reference_path"]
            return result_item
        else:
            logger.warning(
                f"{__class__.__name__} only handle item: {FileDownloadedResultItem.__name__}"
            )
