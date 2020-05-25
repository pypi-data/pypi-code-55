from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()


class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True, nullable=False)
    key = Column(String(8), nullable=False)
    date = Column(DateTime, nullable=False)
    size = Column(Integer, nullable=False)
    expire = Column(DateTime, nullable=False)
    title = Column(String(60), nullable=False)
    syntax = Column(String(16), nullable=False)
    user = Column(String(20), nullable=False)
    scrape_url = Column(String(64), nullable=False)
    full_url = Column(String(32), nullable=False)

    def __repr__(self) -> str:
        return "".join(
            [
                f"<Metadata(",
                f"key='{self.key}', ",
                f"size='{self.size}', ",
                f"date='{self.date}', ",
                f"expire='{self.expire}', ",
                f"title='{self.title}', ",
                f")>",
            ]
        )

    @validates("date")
    def validate_date(self, key: str, date: Union[str, int, datetime]) -> datetime:
        if isinstance(date, str):
            date = datetime.utcfromtimestamp(float(date))
        elif isinstance(date, int):
            date = datetime.utcfromtimestamp(float(date))
        assert type(date) is datetime
        return date

    @validates("expire")
    def validate_expire(self, key: str, expire: Union[str, int, datetime]) -> datetime:
        if isinstance(expire, int):
            expire = str(expire)

        if isinstance(expire, str):
            if expire == "0":
                expire = datetime.max
            else:
                expire = datetime.utcfromtimestamp(float(expire))
        assert type(expire) is datetime
        return expire


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, ForeignKey("metadata.id"), primary_key=True, nullable=False)
    body = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f"<Content(id={self.id})>"
