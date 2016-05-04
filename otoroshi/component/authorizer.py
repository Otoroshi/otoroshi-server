# -*- coding: utf-8 -*-
import re

from autobahn import wamp

from .base import Component
from otoroshi.model import Account, Actuator


class AuthorizerComponent(Component):
    @wamp.register(u'com.betamachine.authorizer.actuator')
    def authorize_actuator(self, session, uri, action):
        account = self._session.query(Account).filter(
            Account.username == session['authid']).one()
        actuator = self._session.query(Actuator).filter(
            Actuator.account_username == account.username).one()

        has_right = re.findall(
            r'^com\.betamachine\.actuator\.{}\.(?:.+)\.(high|low|toggle)$'.format(
                actuator.account_username), uri)
        if len(has_right) > 0:
            print "Actuator {} successfully registered {} procedure".format(
                actuator, uri)
            return True

        print "Actuator {} failed to register {} procedure".format(actuator, uri)
        return False
