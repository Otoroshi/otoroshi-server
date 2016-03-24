# -*- coding: utf-8 -*-
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger
from twisted.python.failure import Failure

from .db import Db
from .config import Config
from component.interact import InteractComponent
from component.listener import ListenerComponent
from component.actuator import ActuatorComponent


class OtoroshiSession(ApplicationSession):
    commands = []
    log = Logger()
    otoroshi_config = Config()

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        self.otoroshi_config.from_env(config.extra['otoroshi_config'])

        self.database = Db(self.otoroshi_config)

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register_all()

        for command in self.commands:
            if isinstance(command, Failure):
                print "Failed to register procedure: %s" % command
            else:
                print "registration ID %s: %s" % (
                    command.id, command.procedure)

    @inlineCallbacks
    def register_all(self):
        components = [InteractComponent, ListenerComponent, ActuatorComponent]
        for component in components:
            command = yield self.register(
                component(self))
            self.commands.extend(command)
