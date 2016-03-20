# -*- coding: utf-8 -*-
import json
from autobahn import wamp
from .base import Component
from otoroshi_server.model import Listener


class ListenerComponent(Component):
    @wamp.register(u'com.betamachine.listener.list')
    def list(self):
        """ List all registered listeners
        """
        listeners = self._session.query(Listener).all()
        return [l.to_json() for l in listeners]

    @wamp.register(u'com.betamachine.listener.create')
    def create(self, id, name):
        """ Create a listener
        """
        listener = Listener(id=id, name=name)
        self._session.add(listener)
        self._session.commit()
        return True

    @wamp.register(u'com.betamachine.listener.delete')
    def delete(self, id):
        """ Delete a listener from the database
        """
        listener = self._session.query(Listener).filter(Listener.id == id)
        is_exist = self._session.query(listener.exists()).scalar()
        if is_exist:
            listener.delete()

        return True
