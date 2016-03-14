from twisted.internet.defer import inlineCallbacks
from twisted.python.failure import Failure
from autobahn.twisted.wamp import ApplicationSession

from otoroshi_server.component.interact import InteractComponent


class OtoroshiComponent(ApplicationSession):
    """
    Otoroshi Server Component that register all RPC and PUBSUB endpoints
    """

    commands = []

    @inlineCallbacks
    def onJoin(self, details):
        yield self.registerAll()

        for command in self.commands:
            if isinstance(command, Failure):
                print "Failed to register procedure: %s" % command
            else:
                print "registration ID %s: %s" % (
                    command.id, command.procedure)

    @inlineCallbacks
    def registerAll(self):
        interact = yield self.register(InteractComponent())
        self.commands.extend(interact)
