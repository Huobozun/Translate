from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pubmed.db.db_models import Reference, PageCrawled
from scrapy.utils.project import get_project_settings


class DbEngine:
    settings = get_project_settings()

    database = settings["SQLITE_DB"]
    dbengigne = create_engine(database)
    session = sessionmaker(dbengigne)()
    Reference.__table__.create(dbengigne, checkfirst=True)
    PageCrawled.__table__.create(dbengigne, checkfirst=True)
