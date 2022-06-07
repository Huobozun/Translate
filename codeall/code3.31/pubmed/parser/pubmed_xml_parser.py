"""
Parsers for MEDLINE XML
reference: https://github.com/titipata/pubmed_parser/blob/master/pubmed_parser/medline_parser.py

"""

import logging
from datetime import datetime
import os
from lxml import etree
from pubmed.parser.utils import (
    read_xml,
    stringify_children,
    attribute_add,
    element_loop,
    get_node_text,
)
from pubmed.utils.time_utils import trace_time_elapsed

logger = logging.getLogger(__name__)


class PubmedXmlParser:
    @classmethod
    @trace_time_elapsed(logger=logger)
    def parse_pubmed_xml_gz(self, path):
        """
        Examples
        --------
        >>> pubmed_parser.parse_medline_xml('data/pubmed20n0014.xml.gz')
        """
        tree = read_xml(path)
        deleted_citations = self.parse_deleted_citations(tree)
        book_articles = self.parse_pubmed_book_article_set(tree)
        articles = self.parse_pubmed_article_set(tree)
        article_ids = self.parse_pubmed_article_id_set(tree)
        result = {
            "deleted_citations": deleted_citations,
            "book_articles": book_articles,
            "articles": articles,
            "articles_ids": article_ids,
            "file_path": os.path.basename(path),
        }
        return result

    @classmethod
    def pubmed_article_to_dict(self, article, source_path=""):
        pmid = self.parse_pmid(article)
        doi = self.parse_doi(article)
        nct_ids = self.parse_ntc_id(article)
        author = self.parse_author_affiliation(article)
        title = self.parse_title(article)
        abstract = self.parse_abstractions(article)
        keywords = self.parse_keywords(article)
        databanks = self.parse_databanks(article)
        article_links = self.parse_article_links(article)
        references = self.parse_references(article)
        medline_journal_info = self.parse_medline_journal_info(article)
        article_journal = self.parse_article_journal(article)
        publication_types = self.parse_publication_types(article)
        mesh_terms = self.parse_mesh_terms(article)
        chemicals = self.parse_chemical_list(article)
        history = self.parse_history(article)
        coi_statement = self.parse_coi_statement(article)
        crawler_time = datetime.utcnow().strftime("%Y-%m-%d %X")

        if not source_path:
            source_path = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"

        return {
            "pmid": pmid,
            "doi": doi,
            "nct_ids": nct_ids,
            "author": author,
            "title": title,
            "abstract": abstract,
            "keywords": keywords,
            "databanks": databanks,
            "article_links": article_links,
            "references": references,
            "medline_journal_info": medline_journal_info,
            "article_journal": article_journal,
            "publication_types": publication_types,
            "mesh_terms": mesh_terms,
            "chemicals": chemicals,
            "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}",
            "crawler_time": crawler_time,
            "source_path": source_path,
            "history": history,
            "coi_statement": coi_statement
        }

    @classmethod
    def pubmed_references_to_list(self, article):
        result = []
        ref_from = self.parse_pmid(article)
        if ref_from:
            references = self.parse_references(article)
            for reference in references:
                ref_to = reference["pmid"]
                if ref_to:
                    result.append({"ref_from": ref_from, "ref_to": ref_to})
        return result

    @classmethod
    def parse_deleted_citations(self, tree):
        deleted_citations = tree.findall(".//DeleteCitation/PMID")
        return [
            {"pmid": get_node_text(pmid), "deleted": True} for pmid in deleted_citations
        ]

    @classmethod
    def parse_pubmed_article_set(self, tree):
        pubmed_articles = tree.findall(".//PubmedArticle")
        return pubmed_articles

    @classmethod
    def parse_pubmed_article_id_set(self, tree):
        pmids = tree.findall(".//PubmedArticle/MedlineCitation/PMID")
        return [{"pmid": get_node_text(pmid)} for pmid in pmids]

    @classmethod
    def parse_pubmed_book_article_set(self, tree):
        pubmed_book_articles = tree.findall(".//PubmedBookArticle")
        return pubmed_book_articles

    @classmethod
    def parse_pmid(self, pubmed_article):
        medline = pubmed_article.find("MedlineCitation")
        if medline.find("PMID") is not None:
            pmid = get_node_text(medline.find("PMID"))
            return pmid
        return ""

    @classmethod
    def parse_doi(self, pubmed_article):
        medline = pubmed_article.find("MedlineCitation")
        article = medline.find("Article")
        elocation_ids = article.findall("ELocationID")

        if len(elocation_ids) > 0:
            for e in elocation_ids:
                doi = get_node_text(e) if e.attrib.get("EIdType", "") == "doi" else ""
        else:
            article_ids = pubmed_article.find("PubmedData/ArticleIdList")
            if article_ids is not None:
                doi = article_ids.find("ArticleId[@IdType='doi']")
                doi = get_node_text(doi)
            else:
                doi = ""
        return doi

    @classmethod
    def parse_ntc_id(self, pubmed_article):
        ntc_ids = []
        databanks = pubmed_article.findall(
            "MedlineCitation/Article/DataBankList/DataBank"
        )
        for databank in databanks:
            databank_name = databank.find("DataBankName")
            databank_name_text = get_node_text(databank_name)
            if databank_name_text == "ClinicalTrials.gov":
                for accession_number in databank.findall(
                    "AccessionNumberList/AccessionNumber"
                ):
                    number = get_node_text(accession_number)
                    if number:
                        ntc_ids.append(
                            {
                                "text": number,
                                "url": f"https://clinicaltrials.gov/ct2/show/{number}",
                            }
                        )
        return ntc_ids

    @classmethod
    def parse_medline_journal_info(self, pubmed_article):
        journal_info = pubmed_article.find("MedlineCitation/MedlineJournalInfo")
        if journal_info is not None:
            medline_ta = get_node_text(journal_info.find("MedlineTA"))
            nlm_unique_id = get_node_text(journal_info.find("NlmUniqueID"))
            issn_linking = get_node_text(journal_info.find("ISSNLinking"))
            country = get_node_text(journal_info.find("Country"))
        else:
            medline_ta = ""
            nlm_unique_id = ""
            issn_linking = ""
            country = ""
        dict_info = {
            "medline_ta": medline_ta,
            "nlm_unique_id": nlm_unique_id,
            "issn_linking": issn_linking,
            "country": country,
        }
        return dict_info

    @classmethod
    def parse_keywords(self, pubmed_article):
        keyword_lists = pubmed_article.findall("MedlineCitation/KeywordList")
        keywords = []
        for keyword_list in keyword_lists:
            for k in keyword_list.findall("Keyword"):
                keyword = get_node_text(k)
                if keyword:
                    keywords.append(keyword)
        return keywords

    @classmethod
    def parse_article_journal(self, pubmed_article):
        journal = pubmed_article.find("MedlineCitation/Article/Journal")
        temp = {}
        attribute_add(journal, temp, "")
        element_l = list(journal)
        return element_loop(element_l, temp, "")

    @classmethod
    def parse_abstractions(self, pubmed_article):
        abstracts = pubmed_article.findall(
            "MedlineCitation/Article/Abstract/AbstractText"
        )
        if abstracts is None or len(abstracts) == 0:
            return [{}]
        result = []
        for abstract in abstracts:
            temp = {}
            attribute_add(abstract, temp, "")
            temp["text"] = stringify_children(abstract).strip() or ""
            result.append(temp)
        return result

    @classmethod
    def parse_publication_types(self, pubmed_article):
        publication_types = []
        publication_type_list = pubmed_article.findall(
            "MedlineCitation/Article/PublicationTypeList/PublicationType"
        )
        if publication_type_list is not None:
            for publication_type in publication_type_list:
                result = {}
                attribute_add(publication_type, result, "")
                text = get_node_text(publication_type)
                ui = result["UI"]
                result["text"] = text
                search_term = f"{ui}[MeSH+Unique+ID]"
                result["url"] = f"https://www.ncbi.nlm.nih.gov/mesh?term={search_term}"
                publication_types.append(result)
        return publication_types

    @classmethod
    def parse_mesh_terms(self, pubmed_article):
        mesh_term = []
        mesh_term_list = pubmed_article.findall(
            "MedlineCitation/MeshHeadingList/MeshHeading/DescriptorName"
        )
        for mesh_term_node in mesh_term_list:
            result = {}
            attribute_add(mesh_term_node, result, "")
            ui = result["UI"]
            text = get_node_text(mesh_term_node)
            result["text"] = text
            search_term = f"{ui}[MeSH+Unique+ID]"
            result["url"] = f"https://www.ncbi.nlm.nih.gov/mesh?term={search_term}"
            result["type"] = "Descriptor"
            mesh_term.append(result)
        mesh_term_list = pubmed_article.findall(
            "MedlineCitation/MeshHeadingList/MeshHeading/QualifierName"
        )
        for mesh_term_node in mesh_term_list:
            result = {}
            attribute_add(mesh_term_node, result, "")
            ui = result["UI"]
            text = get_node_text(mesh_term_node)
            result["text"] = text
            search_term = f"{ui}[MeSH+Unique+ID]"
            result["url"] = f"https://www.ncbi.nlm.nih.gov/mesh?term={search_term}"
            result["type"] = "Qualifier"
            mesh_term.append(result)

        return mesh_term

    @classmethod
    def parse_chemical_list(self, pubmed_article):
        chemical_list = []
        chemicals = pubmed_article.findall("MedlineCitation/ChemicalList/Chemical")
        for chemical in chemicals:
            result = {}
            substance = chemical.find("NameOfSubstance")
            registry_number = chemical.find("RegistryNumber")
            if registry_number is not None:
                attribute_add(registry_number, result, "RegistryNumber")
                result["RegistryNumber"] = get_node_text(registry_number)
            if substance is not None:
                attribute_add(substance, result, "Substance")
                result["Substance"] = get_node_text(substance)
                ui = result["Substance_UI"]
                search_term = f"{ui}[MeSH+Unique+ID]"
                result[
                    "Substance_Url"
                ] = f"https://www.ncbi.nlm.nih.gov/mesh?term={search_term}"
            chemical_list.append(result)

        return chemical_list

    @classmethod
    def parse_databanks(self, pubmed_article):

        results = []
        databanks = pubmed_article.findall(
            "MedlineCitation/Article/DataBankList/DataBank"
        )
        for databank in databanks:
            databank_name = databank.find("DataBankName")
            if databank_name is not None:
                databank_name_text = get_node_text(databank_name)
                accession_numbers = []
                for accession_number in databank.findall(
                    "AccessionNumberList/AccessionNumber"
                ):
                    number = get_node_text(accession_number)
                    if number:
                        accession_numbers.append(number)
                if databank_name_text and accession_numbers:
                    results.append(
                        {
                            "databank_name": databank_name_text,
                            "accession_numbers": accession_numbers,
                        }
                    )
        return results

    @classmethod
    def parse_title(self, pubmed_article):
        title = ""
        title_node = pubmed_article.find("MedlineCitation/Article/ArticleTitle")
        if title_node is not None:
            title = stringify_children(title_node).strip() or ""
        return title

    @classmethod
    def parse_author_affiliation(self, pubmed_article):
        authors = []
        article = pubmed_article.find("MedlineCitation/Article")
        if article is not None:
            author_list = article.find("AuthorList")
            if author_list is not None:
                authors_list = author_list.findall("Author")
                for author in authors_list:
                    forename = get_node_text(author.find("ForeName"))
                    initials = get_node_text(author.find("Initials"))
                    lastname = get_node_text(author.find("LastName"))
                    identifier = get_node_text(author.find("Identifier"))

                    if author.find("AffiliationInfo/Affiliation") is not None:
                        affiliation = get_node_text(
                            author.find("AffiliationInfo/Affiliation")
                        )
                        affiliation = affiliation.replace(
                            "For a full list of the authors' affiliations please see the Acknowledgements section.",
                            "",
                        )
                    else:
                        affiliation = ""
                    authors.append(
                        {
                            "lastname": lastname,
                            "forename": forename,
                            "initials": initials,
                            "identifier": identifier,
                            "affiliation": affiliation,
                        }
                    )
        return authors

    @classmethod
    def parse_references(self, pubmed_article):
        references = []
        reference_list_data = pubmed_article.findall(
            "PubmedData/ReferenceList/Reference"
        )
        for ref in reference_list_data:
            citation = ref.find("Citation")
            citation = get_node_text(citation)
            article_ids = ref.find("ArticleIdList")
            pmid = (
                article_ids.find("ArticleId[@IdType='pubmed']")
                if article_ids is not None
                else None
            )
            pmid = get_node_text(pmid)
            article_ids_list = self.parse_article_list(article_ids, pmid)

            references.append(
                {
                    "citation": citation,
                    "pmid": pmid,
                    "article_ids_list": article_ids_list,
                }
            )
        return references

    @classmethod
    def parse_article_links(self, pubmed_article):
        pmid = self.parse_pmid(pubmed_article)

        article_id_list = pubmed_article.find("PubmedData/ArticleIdList")
        return self.parse_article_list(article_id_list, pmid=pmid)

    @classmethod
    def parse_history(self, pubmed_article):
        results = []
        history_list = pubmed_article.findall("PubmedData/History/PubMedPubDate")
        for history in history_list:
            temp = {}
            attribute_add(history, temp, "")
            element_l = list(history)
            data = element_loop(element_l, temp, "")
            results.append(data)
        return results

    @classmethod
    def parse_coi_statement(self, pubmed_article):
        coi_statement = pubmed_article.find("MedlineCitation/CoiStatement")
        if coi_statement is not None:
            return stringify_children(coi_statement).strip() or ""
        return ""

    @classmethod
    def parse_article_list(self, article_id_list, pmid):
        """
        IdType (doi | pii | pmcpid | pmpid | pmc | mid | sici | pubmed | medline | pmcid | pmcbook | bookaccession) 'pubmed' >

        """
        result = []

        url_patterns = {
            "doi": "https://doi.org/%s",
            "pii": "https://linkinghub.elsevier.com/retrieve/pii/%s",
            "pmc": "https://www.ncbi.nlm.nih.gov/pmc/articles/%s",
            "sici": "",
            "pubmed": "https://pubmed.ncbi.nlm.nih.gov/%s",
        }

        if article_id_list is not None:

            for article_id in article_id_list.findall("ArticleId"):
                idType = article_id.attrib.get("IdType", "")

                text = get_node_text(article_id)
                url_pattern = url_patterns.get(idType, "")
                url = ""
                if url_pattern:
                    url = url_pattern % text.strip()
                elif idType in url_patterns.keys():
                    logger.info(
                        f"{idType}:{text} of pmid:{pmid} do not have url pattern"
                    )
                result.append({"idType": idType, "text": text, "url": url})
        return result

    @classmethod
    def xml_to_string(self, node):
        return etree.tostring(node, pretty_print=True).decode("utf-8")
