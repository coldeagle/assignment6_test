from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Bookmark:
    """
    Pure domain bookmark:
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    notes TEXT,
    date_added TEXT NOT NULL
    date_edited TEXT NOT NULL
    """

    def __init__(self, id, title, url, notes, date_added, date_edited) -> None:
        self.events = []  # type: List[events.Event]
        self.id = id
        self.title = title
        self.url = url
        self.notes = notes
        self.date_added = date_added if date_added is None else datetime.utcnow()
        self.date_edited = date_edited if date_edited is None else datetime.utcnow()



# class BookmarkModel(Base):
#     """
#     Declarative SQLA model
#     """

#     __tablename__ = "bookmarks"

#     id = Column(Integer, primary_key=True)
#     title = Column(String(255))
#     url = Column(String(255))
#     notes = Column(String(255))
#     date_added = Column(Date)
