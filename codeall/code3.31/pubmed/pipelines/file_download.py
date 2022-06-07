from datetime import datetime
import logging
from scrapy.pipelines.files import FilesPipeline
from pubmed.items import FileDownloadedResultItem


logger = logging.getLogger(__name__)


class PubmedDownloadPipeline(FilesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        self.settings = settings
        super().__init__(store_uri, download_func, settings)

    def process_item(self, item, spider):
        self.start_time = datetime.now()
        return super().process_item(item, spider)

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name: str = request.url.split("/")[-1]
        return file_name

    def item_completed(self, results, item, info):
        super().item_completed(results, item, info)
        _, result = results[0]
        result_item = FileDownloadedResultItem()
        now = datetime.now()
        start_time = item.get("start_time", now)
        delta = now - self.start_time
        url = result["url"]
        logger.info(
            f"download {url} took {delta.total_seconds()} secs  start_time: {start_time} to {now}"
        )
        result_item["path"] = result["path"]
        result_item["url"] = result["url"]
        return result_item
