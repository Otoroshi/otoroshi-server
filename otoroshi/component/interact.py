# -*- coding: utf-8 -*-
""" Interact module provide a procedure to bridge listener with actuator.
"""

from autobahn import wamp
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.types import RegisterOptions

from otoroshi.component import Component
from otoroshi.model import Card, Listener


class InteractComponent(Component):  # pylint: disable=R0903
    """ Interact Component, bridge the actuators and listeners
    by providing a procedure to call actuators when listeners
    are triggered.
    """
    REGISTER_OPTIONS = RegisterOptions(details_arg='details')

    @wamp.register(u'io.otoroshi.interact')
    def interact(self, args, details=None):
        """ The interact procedure is called when a client interact with
        a listener, if the client has the correct access right the actuator
        associated with the listener is triggered.

        Args:
            args (dict): Any arguments passed by the caller.
            details (autobahn.wamp.types.SessionDetails): Session informations.

        Raise:
            ApplicationError: An application error if the authentication
            failed (io.otoroshi.authenticate_card.failed as error) or if
            the interact method got a problem (io.otoroshi.interact.failed
            as error).
        """
        try:
            # Retrieve the listener associated with the caller node.
            if details and details.caller_authid:
                caller = self._session.query(Listener).filter(
                    Listener.account_username == details.caller_authid)
                listener = caller.one()
            # Retrieve the card id send by the listener as param.
            if args and args['card']:
                card = self._session.query(Card).filter(
                    Card.id == args['card'])
                card = card.one()
        except:
            raise ApplicationError("com.betamahine.authenticate_card.failed")

        try:
            # Try to interact with the actuator associated to the listener.
            print "AUTH Request to %s(%s) from %s" % (listener.actuator, listener, card)
            yield self._app.call('io.otoroshi.actuator.%s.%s.toggle' % (
                listener.actuator.account_username, listener.actuator_channel))
        except:
            raise ApplicationError("io.otoroshi.interact.failed")
