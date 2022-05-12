import logging
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from pubmed.persist.spider_status_connector import KafkaSpiderStatusConnector
from pubmed.items import FileDownloadingItem
from pubmed.utils.spider_utils import (
    EnviromentAwareSpider,
    MAIN_TEST_ITEM_PIPELINES,
    MAIN_ITEM_PIPELINES,
)
from scrapy.utils.project import get_project_settings

logger = logging.getLogger(__name__)


class TestSpider(EnviromentAwareSpider):
    """
    this spider is used to
    1. debug the spilder logic
    2. calculate the execution time of main spiders: pubmed.annualbaseline and pubmed.dailyupdate,
    after run this spider, run spider pubmed.additional to calcuate it's execution time
    """
    name = "pubmed.test_disable_kafka"
    start_urls = [
        "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/",
        "https://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/",
    ]
    custom_settings = {
        "ITEM_PIPELINES": MAIN_TEST_ITEM_PIPELINES,
    }
    setting = dict(get_project_settings())

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
        new_link_urls = []

        # ignore already crawled page
        for link_url in link_urls:
            if link_url in self.crawled_page_url:
                logger.info(f"link_url:{link_url} is already crawled")
            else:
                new_link_urls.append(link_url)
        tested = False

        # yield item for url specifed in setting: TEST_GZ_NAMES, urls for TEST_GZ_NAMES could be ignored
        for new_link_url in new_link_urls:
            if new_link_url.split("/")[-1] in self.setting["TEST_GZ_NAMES"]:
                item = FileDownloadingItem()
                item["file_urls"] = [link_url]
                item["start_time"] = int(round(datetime.now().timestamp()))
                tested = True
                yield item

        # if no item is yield before, pick one new_link_url for test
        if not tested and len(new_link_urls) > 0:
            item = FileDownloadingItem()
            item["file_urls"] = [new_link_urls[0]]
            item["start_time"] = int(round(datetime.now().timestamp()))

            yield item


class TestEnableKafkaSpider(TestSpider):
    name = "pubmed.test_enable_kafka"
    custom_settings = {
        "ITEM_PIPELINES": MAIN_ITEM_PIPELINES,
    }
