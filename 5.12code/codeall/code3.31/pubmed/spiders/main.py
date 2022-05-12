import logging
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
from pubmed.persist.spider_status_connector import KafkaSpiderStatusConnector

from pubmed.items import FileDownloadingItem
from pubmed.utils.spider_utils import (
    EnviromentAwareSpider,
    MAIN_ITEM_PIPELINES,
    ONLY_DOWNLOAD_ITEM_PIPELINES,
)

logger = logging.getLogger(__name__)


class AnnualBaselineSpider(EnviromentAwareSpider):
    name = "pubmed.annualbaseline"
    start_urls = ["https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"]
    custom_settings = {"ITEM_PIPELINES": MAIN_ITEM_PIPELINES}

    def __init__(self, env="test", name=None, **kwargs):
        super().__init__(env, name, **kwargs)
        self.spilder_status_connector = KafkaSpiderStatusConnector(
            self.kafka_host, dict(get_project_settings())
        )
        self.crawled_page_url = self.spilder_status_connector.get_crawled_page()

    def parse(self, response):
        extractor = LinkExtractor(allow=r"pubmed\d+n\d+.xml.gz$")
        link_urls = [link.url for link in extractor.extract_links(response)]
        link_urls.sort()
        for link_url in link_urls:
            if link_url not in self.crawled_page_url:
                item = FileDownloadingItem()
                item["file_urls"] = [link_url]
                item["start_time"] = int(round(datetime.now().timestamp()))
                yield item
            else:
                logger.info(
                    f"[{self.__class__.__name__}] link_url:{link_url} is already crawled"
                )


class DailyUpdateSpider(AnnualBaselineSpider):
    name = "pubmed.dailyupdate"
    start_urls = ["https://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/"]


class OnlyDownloadSpider(AnnualBaselineSpider):
    name = "pubmed.download_only"
    custom_settings = {
        "ITEM_PIPELINES": ONLY_DOWNLOAD_ITEM_PIPELINES,
        "CONCURRENT_ITEMS": 8,
    }
    start_urls = [
        "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/",
        "https://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/",
    ]

    def __init__(self, env="test", name=None, **kwargs):
        super().__init__(env, name, **kwargs)
        self.crawled_page_url = []


class RerunSpider(AnnualBaselineSpider):
    name = "pubmed.rerun_one_batch"
    custom_settings = {
        "ITEM_PIPELINES": MAIN_ITEM_PIPELINES,
    }
    start_urls = [
        "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/",
        "https://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/",
    ]

    def __init__(self, env="test", batch_name="", name=None, **kwargs):
        super().__init__(env, name, **kwargs)
        self.rerun_batch_name = batch_name

    def parse(self, response):
        extractor = LinkExtractor(allow=r"pubmed\d+n\d+.xml.gz$")
        link_urls = [link.url for link in extractor.extract_links(response)]
        link_urls.sort()
        for link_url in link_urls:
            if link_url.split("/")[-1] == self.rerun_batch_name:
                item = FileDownloadingItem()
                item["file_urls"] = [link_url]
                item["start_time"] = int(round(datetime.now().timestamp()))
                yield item
