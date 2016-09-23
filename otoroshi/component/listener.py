# -*- coding: utf-8 -*-
""" Listener module provide all related procedures and events related to
listeners.
"""

from autobahn import wamp

from otoroshi.component import Component
from otoroshi.model import Listener


class ListenerComponent(Component):
    """ Listener Component, is used to provide some management endpoints for
    listeners.
    """
    @wamp.register(u'io.otoroshi.listener.list')
    def list(self):
        """ List all registered listeners
        """
        listeners = self._session.query(Listener).all()
        return [l.to_json() for l in listeners]

    @wamp.register(u'io.otoroshi.listener.create')
    def create(self, id, name):  # pylint: disable=C0103,W0622
        """ Create a listener.

        Args:
            id (int): Id of the listener.
            name (str): Name of the listener.

        Returns:
            True if the create operation succeed.
        """
        listener = Listener(id=id, name=name)
        self._session.add(listener)
        self._session.commit()
        return True

    @wamp.register(u'io.otoroshi.listener.delete')
    def delete(self, id):  # pylint: disable=C0103,W0622
        """ Delete a listener from the database.

        Args:
            id (int): Id of the listener.

        Returns:
            True if the delete operation succeed.
        """
        listener = self._session.query(Listener).filter(Listener.id == id)
        is_exist = self._session.query(listener.exists()).scalar()
        if is_exist:
            listener.delete()

        return True
