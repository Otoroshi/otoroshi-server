# -*- coding: utf-8 -*-
""" Otoroshi Server is the main component of an Otoroshi Network. It provides
some management methods (for listeners, card reader ...), when a reader ask for
interaction the server verify access of the card and trigger the associated
actuator.
"""
from os import environ

from autobahn.twisted.wamp import ApplicationRunner
from .component import ComponentManager
from .config import Config
from .db import Db


class Otoroshi(object):
    """ The Otoroshi object implement a simple Autobahn application and act as
    the central object. Once it is created it will act as a central registry
    the Components, Configurations, Databases and much more.

    Usually you create a :class:`Otoroshi` instance in your main module or
    in the :file:`__init__.py` file of your package like this::

        from otoroshi_server import Otoroshi
        app = Otoroshi()
    """
    application = None
    config = Config()
    database = Db()

    def run(self):
        """ Start the database connection and run the autobahn application with
        component manager.
        """
        self.database.init_app(self)
        self.application = ApplicationRunner(
            self.config.get('autobahn', 'rooter'),
            self.config.get('autobahn', 'realm'),
            debug=False,
            extra={"app": self})
        self.application.run(ComponentManager)
