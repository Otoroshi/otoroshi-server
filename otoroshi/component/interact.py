# -*- coding: utf-8 -*-
from autobahn import wamp
from autobahn.wamp.types import RegisterOptions
from autobahn.wamp.exception import ApplicationError

from .base import Component
from otoroshi.model import Card, Listener


class InteractComponent(Component):
    _REGISTER_OPTIONS = RegisterOptions(details_arg='details')

    @wamp.register(u'com.betamachine.interact')
    def interact(self, args, details=None):
        try:
            if details and details.caller_authid:
                caller = self._session.query(Listener).filter(
                    Listener.account_username == details.caller_authid)
                listener = caller.one()
            if args and args['card']:
                card = self._session.query(Card).filter(
                    Card.id == args['card'])
                card = card.one()
        except:
            raise ApplicationError("com.betamahine.authenticate_card.failed")

        try:
            print "AUTH Request to %s(%s) from %s" % (listener.actuator, listener, card)
            yield self._app.call('com.betamachine.actuator.%s.%s.toggle' % (
                listener.actuator.account_username, listener.actuator_channel))
        except:
            raise ApplicationError("com.betamachine.interact.failed")
