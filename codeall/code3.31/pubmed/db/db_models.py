from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

db = declarative_base()


class Reference(db):
    __tablename__ = "reference"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    ref_from = Column(Integer)
    ref_to = Column(Integer)

    def __init__(self, ref_from, ref_to) -> None:
        self.ref_from = ref_from
        self.ref_to = ref_to

    def to_dict(self):
        return {c.name: f"{getattr(self, c.name)}" for c in self.__table__.columns}


class PageCrawled(db):
    __tablename__ = "page_crawled"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    page_url = Column(String)

    def __init__(self, page_url) -> None:
        self.page_url = page_url

    def to_dict(self):
        return {c.name: f"{getattr(self, c.name)}" for c in self.__table__.columns}
