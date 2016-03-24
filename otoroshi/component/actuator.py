# -*- coding: utf-8 -*-
import json
from autobahn import wamp
from .base import Component
from otoroshi.model import Actuator


class ActuatorComponent(Component):
    @wamp.register(u'com.betamachine.actuator.list')
    def list(self):
        """ List all registered actuators
        """
        actuators = self._session.query(Actuator).all()
        return [a.to_json() for a in actuators]

    @wamp.register(u'com.betamachine.actuator.create')
    def create(self, id, name):
        """ Create an actuator
        """
        actuator = Actuator(id=id, name=name)
        self._session.add(actuator)
        self._session.commit()
        return True

    @wamp.register(u'com.betamachine.actuator.delete')
    def delete(self, id):
        """ Delete an actuator from the database
        """
        actuator = self._session.query(Actuator).filter(Actuator.id == id)
        is_exist = self._session.query(actuator.exists()).scalar()
        if is_exist:
            actuator.delete()

        return True
