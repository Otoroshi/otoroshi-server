# -*- coding: utf-8 -*-

from sqlalchemy import create_engine  # pylint: disable=F0401
from sqlalchemy.exc import OperationalError  # pylint: disable=F0401
from sqlalchemy.ext.declarative import declarative_base  # pylint: disable=F0401
from sqlalchemy.orm import scoped_session, sessionmaker  # pylint: disable=F0401


BaseModel = declarative_base()  # pylint: disable=C0103


class Db(object):
    def __init__(self, config):
        self.config = config
        self.engine = create_engine(self.config.get('database', 'dsn'))
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = scoped_session(self.session_maker)

    def drop_all(self):
        try:
            BaseModel.metadata.drop_all(self.engine)
        except OperationalError:
            pass

    def create_all(self):
        BaseModel.metadata.create_all(self.engine)
