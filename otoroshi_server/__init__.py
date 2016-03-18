# -*- coding: utf-8 -*-
from os import environ

from autobahn.twisted.wamp import ApplicationRunner
from sqlalchemy import create_engine
from .config import Config
from .component import ComponentManager
from .db import Db
from .model import *


class Otoroshi(object):
    """ The Otoroshi object implement a simple Autobahn application and act as
    the central object. Once it is created it will act as a central registry
    the Components, Configurations, Databases and much more.

    Usually you create a :class:`Otoroshi` instance in your main module or
    in the :file:`__init__.py` file of your package like this::

        from otoroshi_server import Otoroshi
        app = Otoroshi()
    """
    config = Config()
    db = Db()

    def run(self):
        self.db.init_app(self)
        self.application = ApplicationRunner(
            self.config.get('autobahn', 'rooter'),
            self.config.get('autobahn', 'realm'),
            debug=False,
            extra={"app": self})
        self.application.run(ComponentManager)
