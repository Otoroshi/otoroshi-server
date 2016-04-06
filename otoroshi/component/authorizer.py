# -*- coding: utf-8 -*-
from autobahn import wamp
from autobahn.wamp.exception import ApplicationError

from .base import Component
from otoroshi.model import Account


class AuthorizerComponent(Component):
    @wamp.register(u'com.betamachine.authorizer.actuator_manager')
    def authorize_actuator_manager(self, session, uri, action):
        print("Actuator Manager ask for authorize : {}, {}, {}".format(
            session, uri, action))
        return True
