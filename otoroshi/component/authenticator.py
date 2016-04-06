# -*- coding: utf-8 -*-
from autobahn import wamp
from autobahn.wamp.exception import ApplicationError

from .base import Component
from otoroshi.model import Account


class AuthenticatorComponent(Component):
    @wamp.register(u'com.betamachine.authenticate')
    def authenticate(self, realm, authid, details=None):
        account = self._session.query(Account).filter(
            Account.username == authid)

        is_exist = self._session.query(account.exists()).scalar()
        if is_exist:
            account_obj = account.one()
            if account_obj.secret == details['ticket']:
                return account_obj.role

        raise ApplicationError(
            "com.betamachine.auth_failed",
            "could not authenticate session for {}".format(authid))
