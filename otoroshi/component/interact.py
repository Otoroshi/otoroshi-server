# -*- coding: utf-8 -*-
from autobahn import wamp
from .base import Component


class InteractComponent(Component):
    @wamp.register(u'com.betamachine.interact')
    def interact(self, args):
        print "AUTH Request %s" % (args)
