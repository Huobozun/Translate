# Scrapy settings for pubmed project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
from pubmed.utils.env_utils import get_env_variable

BOT_NAME = "pubmed"

SPIDER_MODULES = ["pubmed.spiders"]
NEWSPIDER_MODULE = "pubmed.spiders"

LOG_ENABLED = True
LOG_FORMAT = "%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s: %(message)s"
LOG_LEVEL = "INFO"

ROBOTSTXT_OBEY = False

CONCURRENT_ITEMS = 1

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    "pubmed.middlewares.PubmedDownloaderMiddleware": 543,
    "pubmed.middlewares.TooManyRequestsRetryMiddleware": 544,
}

DOWNLOAD_TIMEOUT = 30001

DOWNLOAD_DELAY = random.random() + random.random()
# 发完一个请求 随机暂停一下 在发下一个请求
RANDOMIZE_DOWNLOAD_DELAY = True

COOKIES_ENABLED = False

FILES_STORE = "/downloads/pubmed/"

# User defined Settings

REMOTE_PERTSIST_TYPE = "empty"  # oss | empty

OSS_STORE = {
    "Endpoint": "http://oss-cn-shanghai.aliyuncs.com",
    "Bucket": "pharmcube-pubmed",
    "AccessKeyId": get_env_variable("ossAccessKeyId"),
    "AccessKeySecret": get_env_variable("ossAccessKeySecret"),
}

KAFKA_TO_ES = {"KafkaTopic": "pharmcube-pubmed-to-es", "EsIndex": "pharmcube-pubmed"}

KAFKA_CRAWELD_PAGE = {
    "KafkaTopic": "pharmcube-pubmed-splider-status",
    "NextMainJobConsumeGroup": "pharmcube-pubmed-crawled-pages",
    "AdditionalFieldJobGroup": "pharmcube-pubmed-additional-field-job",
    "MaxPollRecords": 10000,
}

EXAMPLE_PMIDS = ["3492167"]

TEST_GZ_NAMES = ["pubmed22n1065.xml.gz"]
