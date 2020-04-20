import sqlalchemy as sa
from sqlalchemy import Column, String, Integer

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from settings import DB_HOST, DB_BASE, DB_LOGIN, DB_PASS

Base = declarative_base()


class Speech(Base):
    __tablename__ = "speech"
    id = Column(Integer, primary_key=True)
    body = Column(String(4000))
    meta = Column(String(1000))


def create_engine():
    return sa.create_engine('mysql://{}:{}@{}/{}'.format(DB_LOGIN, DB_PASS, DB_HOST, DB_BASE))


def upload_dialogs(rows):
    engine = create_engine()
    meta = sa.MetaData()




