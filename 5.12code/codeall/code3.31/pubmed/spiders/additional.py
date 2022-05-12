import logging
import os
import json
import scrapy
from datetime import datetime
import numpy as np
from scrapy.utils.project import get_project_settings
from pubmed.persist.spider_status_connector import KafkaSpiderStatusConnector
from pubmed.items import CiteByItem, LinkOutItem, SimilarArticleItem
from pubmed.utils.spider_utils import (
    EnviromentAwareSpider,
    get_random_user_agent,
    ADDITIONAL_ITEM_PIPELINES
)
from pubmed.utils.serialize_utils import JsonSerializer

logger = logging.getLogger(__name__)


class AdditionalSpider(EnviromentAwareSpider):
    name = "pubmed.additional"
    custom_settings = {"ITEM_PIPELINES": ADDITIONAL_ITEM_PIPELINES}
    setting = dict(get_project_settings())

    citeby_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&linkname=pubmed_pubmed_citedin&retmode=json&%s"
    simlar_article_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&linkname=pubmed_pubmed&retmode=json&%s"
    linkout_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&cmd=llinks&retmode=json&%s"
    BATCH_SIZE = 100

    def __init__(self, env="test", name=None, **kwargs):
        super().__init__(env, name, **kwargs)
        self.spilder_status_connector = KafkaSpiderStatusConnector(
            self.kafka_host, dict(get_project_settings())
        )
        self.consumer = self.spilder_status_connector.queue_consmer

    def get_citeby_request(self, pmids: list, file_name: str):
        param = "&".join([f"id={pmid}" for pmid in set(pmids)])
        request_url = self.citeby_url_pattern % param
        request = scrapy.Request(request_url, callback=self.parse_citeby)
        request.headers["User-Agent"] = get_random_user_agent()
        request.meta["file_name"] = file_name
        return request

    def get_simlar_article_request(self, pmids: list, file_name: str):
        param = "&".join([f"id={pmid}" for pmid in set(pmids)])
        request_url = self.simlar_article_url_pattern % param
        request = scrapy.Request(request_url, callback=self.parse_similar_article)
        request.headers["User-Agent"] = get_random_user_agent()
        request.meta["file_name"] = file_name
        return request

    def get_linkout_request(self, pmids: list, file_name: str):
        param = "&".join([f"id={pmid}" for pmid in set(pmids)])
        request_url = self.linkout_url_pattern % param
        request = scrapy.Request(request_url, callback=self.parse_linkout)
        request.headers["User-Agent"] = get_random_user_agent()
        request.meta["file_name"] = file_name
        return request

    def start_requests(self):
        # the splider handle maxinum 100 records
        messages = self.consumer.pull_records(
            timeout_seconds=10, hard_commit=True, max_records=100
        )
        if messages is None or len(messages) == 0:
            logger.info(
                f"no new record avaliable in kafka topic:{self.consumer.topic} to run {self.name}"
            )
            return
        for message in messages:
            origin_article_id_path = message.value.get("article_id_path", "")
            article_id_path = self.infer_right_article_id_path(
                self.setting.get("FILES_STORE", ""), origin_article_id_path
            )
            file_name = message.value.get("file_name", "")
            logger.info(
                f"get additional feilds for batch {file_name} using infered_article_id_path: {article_id_path}"
            )
            if article_id_path and file_name:
                article_ids = JsonSerializer.deserilize_records_from_file(
                    article_id_path
                )
                if article_ids is not None:
                    process_groups = article_ids.groupby(
                        np.arange(len(article_ids.index)) // self.BATCH_SIZE
                    )
                    for _, group in process_groups:
                        pmids = group["pmid"].to_list()
                        yield self.get_citeby_request(pmids, file_name)
                        yield self.get_simlar_article_request(pmids, file_name)
                        yield self.get_linkout_request(pmids, file_name)
                else:
                    logger.info(
                        f"cannot read article_ids info from infered_article_id_path:{article_id_path}, origin_article_id_path:{origin_article_id_path}"
                    )
            else:
                logger.info(
                    f"cannot read article_ids info from infered_article_id_path:{article_id_path}, origin_article_id_path:{origin_article_id_path}"
                )

    def parse_citeby(self, response):
        data = json.loads(response.text)
        crawler_time = datetime.utcnow().strftime("%Y-%m-%d %X")
        for record in data.get("linksets", []):
            if record.get("linksetdbs", None):
                pmid = record.get("ids", [{}])[0]
                links = record.get("linksetdbs", [{}])[0].get("links", [])
                if pmid and links:
                    item = CiteByItem()
                    item["file_name"] = response.meta["file_name"]
                    item["pmid"] = pmid
                    item["citedby_crawled"] = {"time": crawler_time, "pmids": links}
                    yield item

    def parse_similar_article(self, response):
        data = json.loads(response.text)
        crawler_time = datetime.utcnow().strftime("%Y-%m-%d %X")
        for record in data.get("linksets", []):
            if record.get("linksetdbs", None):
                pmid = record.get("ids", [{}])[0]
                links = record.get("linksetdbs", [{}])[0].get("links", [])
                if pmid and links:
                    item = SimilarArticleItem()
                    item["file_name"] = response.meta["file_name"]
                    item["pmid"] = pmid
                    item["similar_articles_crawled"] = {
                        "time": crawler_time,
                        "pmids": links,
                    }
                    yield item

    def parse_linkout(self, response):
        data = json.loads(response.text)
        crawler_time = datetime.utcnow().strftime("%Y-%m-%d %X")
        for record in data.get("linksets", []):
            if record.get("idurllist", None):
                idurllist = record["idurllist"][0]
                pmid = idurllist.get("id", "")
                linkouts = []
                if pmid:
                    links = record.get("idurllist", [{}])[0].get("objurls", [])
                    for link in links:
                        url = link.get("url", {}).get("value", "")
                        categories = ";".join(link.get("categories", []))
                        attributes = ";".join(link.get("attributes", []))
                        linkouts.append(
                            {
                                "url": url,
                                "categories": categories,
                                "attributes": attributes,
                            }
                        )
                    if linkouts:
                        item = LinkOutItem()
                        item["file_name"] = response.meta["file_name"]
                        item["pmid"] = pmid
                        item["linkout_crawled"] = {
                            "time": crawler_time,
                            "links": linkouts,
                        }
                        yield item

    def infer_right_article_id_path(self, file_store_root, article_id_path):
        if os.path.isfile(article_id_path):
            return article_id_path
        suffix = article_id_path.split("article_ids/")[-1]
        new_path = os.path.join(file_store_root, "article_ids", suffix)
        if os.path.isfile(new_path):
            return new_path
        else:
            logger.info(
                f"failed to infer article_id_path for {article_id_path} to {new_path} not a file path"
            )
            return ""
