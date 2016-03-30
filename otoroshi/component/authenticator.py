# -*- coding: utf-8 -*-
from autobahn import wamp
from .base import Component


class AuthenticatorComponent(Component):
    @wamp.register(u'com.betamachine.authenticate')
    def authenticate(self, realm, authid, details=None):
        print "AUTH Request from %s" % authid
        return {'role': u'listener'}
