
import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, JSON, Enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from settings import DB_HOST, DB_BASE, DB_LOGIN, DB_PASS

Base = declarative_base()


class Talk(Base):
    __tablename__ = "talk"
    id = Column(Integer, primary_key=True)
    body = Column(String(2000))
    talk_type = Column(String(1))
    meta = Column(JSON)


def create_engine():
    return sa.create_engine('mysql+pymysql://{}:{}@{}/{}'.format(DB_LOGIN, DB_PASS, DB_HOST, DB_BASE))


def upload_talks(talks):
    engine = create_engine()
    meta = sa.MetaData()
    session = Session(bind=engine)
    session.bulk_insert_mappings(Talk, talks)
    session.commit()







