import random

import scrapy
from pubmed.persist.store import EmptyStore
from pubmed.persist.oss_store import OssStore


class EnviromentAwareSpider(scrapy.Spider):
    def __init__(self, env="test", name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.environment = env
        self.kafka_host = KAKFA_HOST_MAP.get(self.environment, [])


REMOTE_STORE_MAP = {
    "": EmptyStore,
    "empty": EmptyStore,
    "oss": OssStore,
}

KAKFA_HOST_MAP = {
    "test": ["localhost:9092"],
    "dev": ["60.205.229.175:9092"],
    "prod_internal": ["172.17.135.151:9092", "172.17.135.150:9092"],
    "prod_external": ["101.201.152.99:9093", "60.205.139.225:9093"],
}


MAIN_ITEM_PIPELINES = {
    "pubmed.pipelines.file_download.PubmedDownloadPipeline": 1,
    "pubmed.pipelines.article_extract.PubmedArticleExtractPipeline": 20,
    "pubmed.pipelines.kafka_connect.PubmedKafkaPipeline": 40,
    "pubmed.pipelines.page_crawled_status.PubmedSavePageCrawledStatusPipeline": 100,
    "pubmed.pipelines.clean_local_file.CleanLocalFilePipeline": 200,
}

MAIN_TEST_ITEM_PIPELINES = {
    "pubmed.pipelines.file_download.PubmedDownloadPipeline": 1,
    "pubmed.pipelines.article_extract.PubmedArticleExtractPipeline": 20,
    "pubmed.pipelines.clean_local_file.CleanLocalFilePipeline": 200,
}

ONLY_DOWNLOAD_ITEM_PIPELINES = {
    "pubmed.pipelines.file_download.PubmedDownloadPipeline": 1,
}

DOWNLOAD_ITEM_PIPELINES = {
    "pubmed.pipelines.file_download.PubmedDownloadPipeline": 1,
}

ADDITIONAL_ITEM_PIPELINES = {
    "pubmed.pipelines.additional_filed_item.PubmedAdditionalFiledItemPipeline": 1,
}

USER_AGENT_LIST = [
    "Mozilla/5.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36",
]


def get_random_user_agent():
    return random.choice(USER_AGENT_LIST)
