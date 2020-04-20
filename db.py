import os
from os.path import expanduser
from typing import List, Dict

import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func

from settings import DB_FPATH

meta = sa.MetaData()
Base = declarative_base(metadata=meta)


class Transcript(Base):
    __tablename__ = "transcript"
    id = Column(Integer, primary_key=True, autoincrement=True)
    transcript = Column(String(5000), nullable=False)
    is_monolog = Column(Integer)
    meta = Column(JSON)


def create_sqlite_engine():
    """ Make engine to connect sqlite"""
    return sa.create_engine('sqlite:///{}'.format(DB_FPATH),
                            connect_args={'check_same_thread': False})


def upload_transcripts(transcripts: List[Dict]):
    """ Upload list of dicts to sqlite """
    engine = create_sqlite_engine()
    session = Session(bind=engine)
    session.bulk_insert_mappings(Transcript, transcripts)
    session.commit()


def load_random_transcript(movie=None):
    """ Load from sqlite transcript"""
    engine = create_sqlite_engine()
    session = Session(bind=engine)
    row = session.query(Transcript).order_by(func.random()).first()
    if not row:
        return 'No transcripts'

    return row.transcript

