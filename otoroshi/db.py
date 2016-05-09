# -*- coding: utf-8 -*-
""" Database integration with SQLAlchemy.
"""

from sqlalchemy import create_engine  # pylint: disable=F0401
from sqlalchemy.exc import OperationalError  # pylint: disable=F0401
from sqlalchemy.ext.declarative import declarative_base  # pylint: disable=F0401
from sqlalchemy.orm import scoped_session, sessionmaker  # pylint: disable=F0401


BaseModel = declarative_base()  # pylint: disable=C0103


class Db(object):
    """ This class provide some helper to work with SQLAlchemy, it is
    lightly inspired from Flask-SQLAlchemy.
    """
    def __init__(self, config):
        """ Configure the database session object.

        Args:
            config (otoroshi.Config): The configuration object where database
                information are stored.
        """
        self.config = config
        self.engine = create_engine(self.config.get('database', 'dsn'))
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = scoped_session(self.session_maker)

    def drop_all(self):
        """ Drop all database data and schema.
        """
        try:
            BaseModel.metadata.drop_all(self.engine)
        except OperationalError:
            pass

    def create_all(self):
        """ Create the database schema.
        """
        BaseModel.metadata.create_all(self.engine)
