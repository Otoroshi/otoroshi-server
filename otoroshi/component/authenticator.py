# -*- coding: utf-8 -*-
""" Authenticator module is responsible of the authentications methods
provided to the client in the Otoroshi crossbar network.
"""

from autobahn import wamp
from autobahn.wamp.exception import ApplicationError

from otoroshi.component import Component
from otoroshi.model import Account


class AuthenticatorComponent(Component):  # pylint: disable=R0903
    """ AuthenticatorComponent is responsible of the authentication in
    the crossbar network.
    """
    @wamp.register(u'io.otoroshi.authenticate')
    def authenticate(self, realm, authid, details=None):  # pylint: disable=W0613
        """ This method is exposed though RPC as a procedure is called by all
        the node trying to join the network. The provided account will
        determin the role assigned to the node.

        Actually, the authentication method used is always by tickets.

        Args:
            realm (str): The realm to client wishes to join (if the client
                did announance a realm).
            authid (str): The authentication ID to authenticate.
            details (autobahn.wamp.types.CallDetails): The details of the
                client.

        Return:
            The role assigned to the client.

        Raise:
            ApplicationError: If the authentication failed.
        """
        account = self._session.query(Account).filter(
            Account.username == authid)

        is_exist = self._session.query(account.exists()).scalar()
        if is_exist:
            account_obj = account.one()
            if account_obj.secret == details['ticket']:
                return account_obj.role

        raise ApplicationError(
            "io.otoroshi.auth_failed",
            "could not authenticate session for {}".format(authid))
