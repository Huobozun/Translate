# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FileDownloadingItem(scrapy.Item):
    file_urls = scrapy.Field()
    start_time = scrapy.Field()
    files = scrapy.Field


class FileDownloadedResultItem(scrapy.Item):
    path = scrapy.Field()
    url = scrapy.Field()


class PubmedArticleSetItem(scrapy.Item):
    article_id_path = scrapy.Field()
    deletion_path = scrapy.Field()
    article_path = scrapy.Field()
    reference_path = scrapy.Field()
    file_path = scrapy.Field()
    file_name = scrapy.Field()
    file_url = scrapy.Field()
    citedby_crawled_path = scrapy.Field()
    simlar_article_crawled_path = scrapy.Field()
    linkout_path = scrapy.Field()


class CiteByItem(scrapy.Item):
    pmid = scrapy.Field()
    file_name = scrapy.Field()
    citedby_crawled = scrapy.Field()


class SimilarArticleItem(scrapy.Item):
    pmid = scrapy.Field()
    file_name = scrapy.Field()
    similar_articles_crawled = scrapy.Field()


class LinkOutItem(scrapy.Item):
    pmid = scrapy.Field()
    file_name = scrapy.Field()
    linkout_crawled = scrapy.Field()
