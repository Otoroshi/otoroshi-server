from autobahn import wamp


class InteractComponent(object):
    @wamp.register(u'com.betamachine.interact')
    def interact(self, args):
        print "AUTH Request %s" % (args)
