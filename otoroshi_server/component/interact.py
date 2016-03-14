from autobahn import wamp


class InteractComponent(object):
    @wamp.register(u'com.betamachine.interact')
    def interact(self, card_id, listener_id):
        print('AUTH Request')
