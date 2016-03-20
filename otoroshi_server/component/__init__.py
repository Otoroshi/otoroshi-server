# -*- coding: utf-8 -*-
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import types
from twisted.internet.defer import inlineCallbacks
from twisted.python.failure import Failure
from .interact import InteractComponent
from .listener import ListenerComponent


class ComponentManager(ApplicationSession):
    """ Otoroshi Server Component Manager that register all RPC and PUBSUB
    endpoints
    """

    commands = []

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
        components = [InteractComponent, ListenerComponent]
        for component in components:
            command = yield self.register(
                component(self.config.extra['app']))
            self.commands.extend(command)
