# -*- coding: utf-8 -*-
""" Authorizer module is responsible of the network autorization like
accepting (or not) :
    - registering or calling procedure,
    - subscribing or publishing to a topic.

It is notably used for actuator that uses dynamic procedure registration
(named with their name).
"""

import re

from autobahn import wamp

from otoroshi.component import Component
from otoroshi.model import Account, Actuator


class AuthorizerComponent(Component):  # pylint: disable=R0903
    """ The component expose all the authorize method called when a
    node try to make an action on the network that need to be verified.
    The authorizer assigned to node is defined by their role in the
    configuration of crossbar.
    """
    @wamp.register(u'io.otoroshi.authorizer.actuator')
    def authorize_actuator(self, session, uri, action):  # pylint: disable=W0613
        """ This method is used to authorize actuator to register their
        procedure to interact with channels. Each actuator can only register
        procedure that follow theses rules :
            - the procedure name must begin with 'io.otoroshi.actuator',
            - followed by the account username of the node,
            - followed by high, low or toggle.

        Args:
            session (autobahn.wamp.protocol.ApplicationSession): The WAMP
                session that requests the action.
            uri (str): The URI on which to perform the action.
            action (str): The action to be performed.

        Return:
            A boolean flag indicating whether session is authorized or not.
        """
        account = self._session.query(Account).filter(
            Account.username == session['authid']).one()
        actuator = self._session.query(Actuator).filter(
            Actuator.account_username == account.username).one()

        has_right = re.findall(
            r'^io\.otoroshi\.actuator\.{}\.(?:.+)\.(high|low|toggle)$'.format(
                actuator.account_username), uri)
        if len(has_right) > 0:
            print("Actuator {} successfully registered {} procedure".format(
                actuator, uri))
            return True

        print("Actuator {} failed to register {} procedure".format(
            actuator, uri))
        return False
