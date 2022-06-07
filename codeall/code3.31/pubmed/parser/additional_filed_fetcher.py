import logging
import math
import multiprocessing
import requests
import pandas as pd
import numpy as np
from tqdm import tqdm
from pandarallel import pandarallel
from datetime import datetime
from pubmed.utils.time_utils import trace_time_elapsed, min_exe_time
from pubmed.utils.serialize_utils import JsonSerializer
from pubmed.parser.pubmed_xml_parser import PubmedXmlParser
tqdm.pandas()

logger = logging.getLogger(__name__)

# according to user guideline https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requirement
# limit the MAX_REQUES_PER_SECOND to 3
MAX_REQUES_PER_SECOND = 3

# according to the ELink API,  get rquest can accepet at most 200 ids
BATCH_SIZE = 200


class HtmlFetcher:
    def __init__(self) -> None:
        # for muliprocess this value will be forked to each subprogresss
        # each subprogress has it's own value
        self.processed_count = 0
        self.all_count = 1

    @min_exe_time(logger=logger, log_level=logging.DEBUG, secs=1)
    def fetch_filed_for_pmid(self, pmid: str, request_url_pattern, filed_name):
        request_url = request_url_pattern % pmid
        response = requests.get(request_url)
        return self.parse_items(response, filed_name=filed_name)

    @min_exe_time(logger=logger, log_level=logging.DEBUG, secs=1)
    def fetch_filed_from_pmids(self, pmids: list, request_url_pattern, filed_name):
        param = "&".join([f"id={pmid}" for pmid in set(pmids)])
        request_url = request_url_pattern % param
        response = requests.get(request_url)
        result = self.parse_items(response, filed_name=filed_name)
        self.increase_process_count()
        return result

    def increase_process_count(self):
        approximate_process_count = math.ceil(self.all_count / MAX_REQUES_PER_SECOND)
        progress_rate = self.processed_count / approximate_process_count
        progress = "{:.2%}".format(progress_rate)
        pid = multiprocessing.current_process().pid
        if math.ceil(progress_rate * 100) % 10 == 0:
            logger.info(
                f"subprocess: {pid}, progress: {progress}, processed_count:{self.processed_count}, subprocess_approximate_count: {approximate_process_count}, all_count:{self.all_count}"
            )
        self.processed_count += 1

    def parse_items(self, response, filed_name):
        results = []
        crawler_time = datetime.utcnow().strftime("%Y-%m-%d %X")
        if response.status_code == 200:
            data = response.json()
            for record in data.get("linksets", []):
                if record.get("linksetdbs", None):
                    results.append(
                        {
                            "pmid": record["ids"][0],
                            filed_name: {
                                "time": crawler_time,
                                "pmids": record["linksetdbs"][0]["links"],
                            },
                        }
                    )
        return results


class CitebyFetcher(HtmlFetcher):
    column_name = "citedby_crawled"
    single_request_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&linkname=pubmed_pubmed_citedin&retmode=json&id=%s"
    batch_request_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&linkname=pubmed_pubmed_citedin&retmode=json&%s"

    @trace_time_elapsed(logger=logger)
    def bactch_fetch_field(self, pmid_info_path) -> list:
        pandarallel.initialize(progress_bar=False, nb_workers=MAX_REQUES_PER_SECOND)
        results = JsonSerializer.deserilize_records_from_file(pmid_info_path)
        process_groups = results.groupby(np.arange(len(results.index)) // BATCH_SIZE)
        self.all_count = len(process_groups.index)
        grouped_results = pd.DataFrame()
        grouped_results["results"] = process_groups.parallel_apply(
            lambda group: self.fetch_filed_from_group(group)
        )
        return grouped_results.explode("results")["results"].to_list()

    @min_exe_time(logger=logger, log_level=logging.DEBUG, secs=1)
    def fetch_filed_from_group(self, group):
        pmids = group["pmid"].to_list()
        return self.fetch_filed_from_pmids(pmids=pmids)

    def fetch_filed_for_pmid(self, pmid: str):
        return super().fetch_filed_for_pmid(
            pmid=pmid,
            request_url_pattern=self.single_request_url_pattern,
            filed_name=self.column_name,
        )

    def fetch_filed_from_pmids(self, pmids: list):
        return super().fetch_filed_from_pmids(
            pmids=pmids,
            request_url_pattern=self.batch_request_url_pattern,
            filed_name=self.column_name,
        )


class SimilarArticleFetcher(HtmlFetcher):
    column_name = "similar_articles_crawled"
    single_request_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&linkname=pubmed_pubmed&retmode=json&id=%s"
    batch_request_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&linkname=pubmed_pubmed&retmode=json&%s"

    @trace_time_elapsed(logger=logger)
    def bactch_fetch_field(self, pmid_info_path) -> list:
        pandarallel.initialize(progress_bar=False, nb_workers=MAX_REQUES_PER_SECOND)
        results = JsonSerializer.deserilize_records_from_file(pmid_info_path)
        process_groups = results.groupby(np.arange(len(results.index)) // BATCH_SIZE)
        self.all_count = len(process_groups.index)
        grouped_results = pd.DataFrame()
        grouped_results["results"] = process_groups.parallel_apply(
            lambda group: self.fetch_filed_from_group(group)
        )
        return grouped_results.explode("results")["results"].to_list()

    @min_exe_time(logger=logger, log_level=logging.DEBUG, secs=1)
    def fetch_filed_from_group(self, group):
        pmids = group["pmid"].to_list()
        return self.fetch_filed_from_pmids(pmids=pmids)

    def fetch_filed_for_pmid(self, pmid: str):
        return super().fetch_filed_for_pmid(
            pmid=pmid,
            request_url_pattern=self.single_request_url_pattern,
            filed_name=self.column_name,
        )

    def fetch_filed_from_pmids(self, pmids: list):
        return super().fetch_filed_from_pmids(
            pmids=pmids,
            request_url_pattern=self.batch_request_url_pattern,
            filed_name=self.column_name,
        )


class LinkOutFetcher(HtmlFetcher):
    column_name = "links"
    single_request_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&cmd=llinks&retmode=json&id=%s"
    batch_request_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&cmd=llinks&retmode=json&%s"

    @trace_time_elapsed(logger=logger)
    def bactch_fetch_field(self, pmid_info_path) -> list:
        pandarallel.initialize(progress_bar=False, nb_workers=MAX_REQUES_PER_SECOND)
        results = JsonSerializer.deserilize_records_from_file(pmid_info_path)
        process_groups = results.groupby(np.arange(len(results.index)) // BATCH_SIZE)
        self.all_count = len(process_groups)
        grouped_results = pd.DataFrame()
        grouped_results["results"] = process_groups.parallel_apply(
            lambda group: self.fetch_filed_from_group(group)
        )
        return grouped_results.explode("results")["results"].to_list()

    @min_exe_time(logger=logger, log_level=logging.DEBUG, secs=1)
    def fetch_filed_from_group(self, group):
        pmids = group["pmid"].to_list()
        return self.fetch_filed_from_pmids(pmids=pmids)

    def fetch_filed_for_pmid(self, pmid: str):
        return super().fetch_filed_for_pmid(
            pmid=pmid,
            request_url_pattern=self.single_request_url_pattern,
            filed_name=self.column_name,
        )

    def fetch_filed_from_pmids(self, pmids: list):
        return super().fetch_filed_from_pmids(
            pmids=pmids,
            request_url_pattern=self.batch_request_url_pattern,
            filed_name=self.column_name,
        )

    def parse_items(self, response, filed_name):
        results = []
        crawler_time = datetime.utcnow().strftime("%Y-%m-%d %X")
        if response.status_code == 200:
            data = response.json()
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
                            results.append(
                                {
                                    "pmid": pmid,
                                    filed_name: {
                                        "time": crawler_time,
                                        "links": linkouts,
                                    },
                                }
                            )
        return results


class ContentFetcher(HtmlFetcher):
    column_name = 'content'
    single_request_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&db=pubmed&retmode=xml&id=%s"
    batch_request_url_pattern = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?dbfrom=pubmed&db=pubmed&retmode=xml&%s"

    @trace_time_elapsed(logger=logger)
    def batch_fetch_from_df(self, data: pd.DataFrame) -> list:
        pandarallel.initialize(progress_bar=False, nb_workers=MAX_REQUES_PER_SECOND)
        process_groups = data.groupby(np.arange(len(data.index)) // BATCH_SIZE)
        self.all_count = len(process_groups)
        grouped_results = pd.DataFrame()
        grouped_results["results"] = process_groups.parallel_apply(
            lambda group: self.fetch_filed_from_group(group)
        )
        return grouped_results.explode("results")["results"].to_list()

    @trace_time_elapsed(logger=logger)
    def bactch_fetch_field(self, pmid_info_path) -> list:
        results = JsonSerializer.deserilize_records_from_file(pmid_info_path)
        return self.batch_fetch_from_df(results)

    @min_exe_time(logger=logger, log_level=logging.DEBUG, secs=1)
    def fetch_filed_from_group(self, group):
        pmids = group["pmid"].to_list()
        return self.fetch_filed_from_pmids(pmids=pmids)

    def fetch_filed_for_pmid(self, pmid: str):
        return super().fetch_filed_for_pmid(
            pmid=pmid,
            request_url_pattern=self.single_request_url_pattern,
            filed_name=self.column_name,
        )

    def fetch_filed_from_pmids(self, pmids: list):
        return super().fetch_filed_from_pmids(
            pmids=pmids,
            request_url_pattern=self.batch_request_url_pattern,
            filed_name=self.column_name,
        )

    def parse_items(self, response, filed_name):
        results = []
        if response.status_code == 200:
            data = response.content
            dict_out = PubmedXmlParser.parse_pubmed_xml_gz(data)
            articles = dict_out['articles']
            for article in articles:
                article_dict = PubmedXmlParser.pubmed_article_to_dict(article)
                results.append(article_dict)
        return results
