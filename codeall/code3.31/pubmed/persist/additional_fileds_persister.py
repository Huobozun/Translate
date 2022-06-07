import logging
from pubmed.utils.serialize_utils import JsonSerializer
from pubmed.persist.store import Store
from pubmed.parser.additional_filed_fetcher import (
    CitebyFetcher,
    LinkOutFetcher,
    SimilarArticleFetcher,
)
from pubmed.utils.time_utils import trace_time_elapsed

logger = logging.getLogger(__name__)


class AdditionalFieldsItemsPersister:
    def __init__(self, local_store: Store, cloud_store: Store) -> None:
        self.loal_store = local_store
        self.cloud_store = cloud_store

    def append(self, data: dict, file_path):
        data_str = JsonSerializer.serilize_one_record(data)
        self.loal_store.append(file_path, data_str)
        self.cloud_store.append(file_path, data_str)

    def append_batch(self, batch: list, file_path):
        data_str = JsonSerializer.serialize_records(batch)
        self.loal_store.append(file_path, data_str)
        self.cloud_store.append(file_path, data_str)


class AdditionalFieldsPersister:
    def __init__(self, local_store: Store, cloud_store: Store) -> None:
        self.loal_store = local_store
        self.cloud_store = cloud_store

    @trace_time_elapsed(logger=logger)
    def save(self, item: dict):
        file_name = item.get("file_name", "").split(".")[0]
        article_id_path = item.get("article_id_path", "")

        # reqeust Citeby and SimilarArticle is time-consuming with multiple http get request
        # try to use local cache to avoid sending get request to pubmed.
        # this major happens when rerun the same splider.
        citedby_crawled_path = f"citedby/crawled/{file_name}.json"
        if not self.loal_store.file_exists(citedby_crawled_path):
            citedby = CitebyFetcher().bactch_fetch_field(article_id_path)
        else:
            citedby = JsonSerializer.deserilize_records_from_file(
                self.loal_store.full_path(citedby_crawled_path)
            ).to_dict(orient="records")
        citedby_crawled_path = self.save_json_array(
            citedby, f"citedby/crawled/{file_name}.json"
        )

        simlar_article_crawled_path = f"simlar_article/crawled/{file_name}.json"
        if not self.loal_store.file_exists(simlar_article_crawled_path):
            simlar_article = SimilarArticleFetcher().bactch_fetch_field(article_id_path)
        else:
            simlar_article = JsonSerializer.deserilize_records_from_file(
                self.loal_store.full_path(simlar_article_crawled_path)
            ).to_dict(orient="records")
        simlar_article_crawled_path = self.save_json_array(
            simlar_article, f"simlar_article/crawled/{file_name}.json"
        )

        linkout_path = f"linkout/crawled/{file_name}.json"
        if not self.loal_store.file_exists(linkout_path):
            linkout = LinkOutFetcher().bactch_fetch_field(article_id_path)
        else:
            linkout = JsonSerializer.deserilize_records_from_file(
                self.loal_store.full_path(linkout_path)
            ).to_dict(orient="records")
        linkout_path = self.save_json_array(
            linkout, f"linkout/crawled/{file_name}.json"
        )

        return {
            "citedby_crawled_path": citedby_crawled_path,
            "simlar_article_crawled_path": simlar_article_crawled_path,
            "linkout_path": linkout_path,
        }

    def save_json_array(self, json_array, file_path):
        records_str = JsonSerializer.serialize_records(json_array)
        if records_str.strip():
            local_path = self.loal_store.save(file_path, records_str)
            self.cloud_store.save(file_path, records_str)
            return local_path
        return ""
