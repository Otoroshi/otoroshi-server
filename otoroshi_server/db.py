# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, scoped_session


BaseModel = declarative_base()


class Db(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.engine = create_engine(self.app.config.get('database', 'dsn'))
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = scoped_session(self.session_maker)

    def drop_all(self):
        try:
            BaseModel.metadata.drop_all(self.engine)
        except OperationalError:
            pass

    def create_all(self):
        BaseModel.metadata.create_all(self.engine)
