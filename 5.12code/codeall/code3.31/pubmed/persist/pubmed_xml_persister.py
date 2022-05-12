import random
import logging
from pubmed.utils.serialize_utils import JsonSerializer
from pubmed.persist.store import Store
from pubmed.parser.pubmed_xml_parser import PubmedXmlParser
from pubmed.utils.time_utils import trace_time_elapsed

logger = logging.getLogger(__name__)


class PubmedXmlPersister:
    def __init__(self, local_store: Store, cloud_store: Store, example_pmids) -> None:
        self.loal_store = local_store
        self.cloud_store = cloud_store
        self.xmlinfo = []
        self.example_pmids = example_pmids

    @trace_time_elapsed(logger=logger)
    def save(self, pubmed_xml_meta: dict):
        file_path = pubmed_xml_meta.get("file_path", "")
        file_name = file_path.split(".")[0]
        parsed_article = []
        reference_set = []
        article_id_path = ""
        deletion_path = ""
        article_path = ""
        reference_path = ""
        example_index = random.randint(0, len(pubmed_xml_meta["articles"]) - 1)
        for index, article in enumerate(pubmed_xml_meta["articles"]):
            parsed_dict, references = self.save_article(
                article, f"articles/xml/{file_name}/%s.xml", example_index == index
            )
            parsed_article.append(parsed_dict)
            reference_set.extend(references)

        article_id_path = self.save_json_array(
            pubmed_xml_meta["articles_ids"], f"article_ids/parsed/{file_name}.json"
        )
        deletion_path = self.save_json_array(
            pubmed_xml_meta["deleted_citations"], f"deletions/parsed/{file_name}.json"
        )
        article_path = self.save_json_array(
            parsed_article, f"articles/parsed/{file_name}.json"
        )
        reference_path = self.save_json_array(
            reference_set, f"references/parsed/{file_name}.json"
        )

        return {
            "article_id_path": article_id_path,
            "deletion_path": deletion_path,
            "article_path": article_path,
            "reference_path": reference_path,
        }

    def save_article(self, article, file_path_patten, as_example):
        pmid = PubmedXmlParser.parse_pmid(article)
        parsed_dict = PubmedXmlParser.pubmed_article_to_dict(article)
        references = PubmedXmlParser.pubmed_references_to_list(article)
        if as_example or pmid in self.example_pmids:
            xml_string = PubmedXmlParser.xml_to_string(article)
            self.loal_store.save(file_path_patten % pmid, xml_string)
            self.cloud_store.save(file_path_patten % pmid, xml_string, overwite=False)
            parsed_dict_str = JsonSerializer.serilize_one_record(parsed_dict)
            self.loal_store.save(f"articles/example/{pmid}.json", parsed_dict_str)
            self.cloud_store.save(
                f"articles/example/{pmid}.json", parsed_dict_str, overwite=False
            )
        return parsed_dict, references

    def save_json_array(self, json_array, file_path):
        records_str = JsonSerializer.serialize_records(json_array)
        if records_str.strip():
            local_path = self.loal_store.save(file_path, records_str)
            self.cloud_store.save(file_path, records_str)
            return local_path
        return ""
