# -*- coding: utf-8 -*-
""" This package provide a crossbar server for Otoroshi application.
"""

from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger
from twisted.python.failure import Failure

from otoroshi.config import Config
from otoroshi.component.actuator import ActuatorComponent
from otoroshi.component.authenticator import AuthenticatorComponent
from otoroshi.component.authorizer import AuthorizerComponent
from otoroshi.component.interact import InteractComponent
from otoroshi.component.listener import ListenerComponent
from otoroshi.db import Db


class OtoroshiSession(ApplicationSession):
    """ Main Otoroshi Server component, this component is in charge of
    registering all the commands and surcharging default behaviors.
    """
    commands = []
    log = Logger()
    otoroshi_config = Config()

    def __init__(self, config=None):
        """ Initialize the Otoroshi server, called on startup it load
        the configuration and the database.

        Args:
            config (str): Name of the ENV variable which contain the config file path.

        Raise:
            RuntimeError: If an invalid configuration file was provided.
        """
        ApplicationSession.__init__(self, config)
        self.otoroshi_config.from_env(config.extra['otoroshi_config'])

        self.database = Db(self.otoroshi_config)

    @inlineCallbacks
    def onJoin(self, details):  # pylint: disable=C0103,W0613
        """ Called when the router has been started.

        Args:
            details (autobahn.wamp.types.SessionDetails): WAMP Session details.
        """
        yield self.register_all()

        for command in self.commands:
            if isinstance(command, Failure):
                print("Failed to register procedure: {}".format(command))
            else:
                print("registration ID {}: {}".format(
                    command.id, command.procedure))

    @inlineCallbacks
    def register_all(self):
        """ Register all the components needed to run Otoroshi properly.
        """
        components = [InteractComponent, ListenerComponent, ActuatorComponent,
                      AuthenticatorComponent, AuthorizerComponent]
        for component in components:
            command = yield self.register(  # pylint: disable=E1101
                component(self),
                options=component.REGISTER_OPTIONS)
            self.commands.extend(command)
