# -*- coding: utf-8 -*-
""" Actuator module provide all related procedures and events related to
actuators.
"""

from autobahn import wamp

from otoroshi.component import Component
from otoroshi.model import Actuator


class ActuatorComponent(Component):
    """ Actuator Component, is used to provide some management endpoints for
    actuators.
    """
    @wamp.register(u'io.otoroshi.actuator.list')
    def list(self):
        """ List all registered actuators.
        """
        actuators = self._session.query(Actuator).all()
        return [a.to_json() for a in actuators]

    @wamp.register(u'io.otoroshi.actuator.create')
    def create(self, id, name):  # pylint: disable=C0103,W0622
        """ Create an actuator.

        Args:
            id (int): Id of the actuator.
            name (str): Name of the actuator.

        Returns:
            True if the create operation succeed.
        """
        actuator = Actuator(id=id, name=name)
        self._session.add(actuator)
        self._session.commit()
        return True

    @wamp.register(u'io.otoroshi.actuator.delete')
    def delete(self, id):  # pylint: disable=C0103,W0622
        """ Delete an actuator from the database.

        Args:
            id (int): Id of the actuator.

        Returns:
            True if the delete operation succeed.
        """
        actuator = self._session.query(Actuator).filter(Actuator.id == id)
        is_exist = self._session.query(actuator.exists()).scalar()
        if is_exist:
            actuator.delete()

        return True
