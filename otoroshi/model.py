# -*- coding: utf-8 -*-
""" This module contain all required data models.
"""

import json

from sqlalchemy import Column, Enum, ForeignKey, String  # pylint: disable=F0401
from sqlalchemy.orm import relationship  # pylint: disable=F0401

from otoroshi.db import BaseModel


class Account(BaseModel):  # pylint: disable=R0903,W0232
    """ Account model that store accounts informations, thoses accounts are
    used to identify the users that try to join the crossbar network.
    """
    __tablename__ = 'accounts'

    username = Column(String(32), primary_key=True, nullable=False)
    secret = Column(String, nullable=False)
    role = Column(
        Enum('admin', 'listener', 'actuator'), nullable=False)

    def __repr__(self):
        return "<Account('%s', '%s')>" % (self.username, self.role)


class Card(BaseModel):  # pylint: disable=R0903,W0232
    """ Card model store informations about cards that are used to trigger a
    listener such as RFID card reader.
    """
    __tablename__ = 'cards'

    id = Column(String(32), primary_key=True)  # pylint: disable=C0103
    shortname = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<Card('%s','%s')>" % (self.id, self.fullname)


class Listener(BaseModel):  # pylint: disable=R0903,W0232
    """ A listener is a thing that listen to event and interact with other
    things. Actually, a listener is representated by a RFID Card Reader and
    ask for actuators to open or close a channel (relay).
    """
    __tablename__ = 'listeners'

    id = Column(String(32), primary_key=True)  # pylint: disable=C0103
    name = Column(String)
    actuator_id = Column(
        String(32), ForeignKey('actuators.id'), nullable=False)
    actuator = relationship('Actuator')
    account_username = Column(
        String(32), ForeignKey('accounts.username'), nullable=False)
    account = relationship('Account')
    actuator_channel = Column(String(32), nullable=False)

    def __repr__(self):
        return "<Listener('%s', '%s')>" % (self.id, self.name)

    def to_json(self):
        """ Transform a listener to a json representation.

        Return:
            A JSON Object.
        """
        return json.dumps({
            "id": self.id,
            "name": self.name
        })


class Actuator(BaseModel):  # pylint: disable=R0903,W0232
    """ An actuator has some channels and provide command to interact
    with them (like openning or closing a door).
    """
    __tablename__ = 'actuators'

    id = Column(String(32), primary_key=True)  # pylint: disable=C0103
    name = Column(String)
    account_username = Column(
        String(32), ForeignKey('accounts.username'), nullable=False)
    account = relationship('Account')

    def __repr__(self):
        return "<Actuator('%s', '%s')>" % (self.id, self.name)

    def to_json(self):
        """ Transform an actuator to a json representation.

        Return:
            A JSON Object.
        """
        return json.dumps({
            "id": self.id,
            "name": self.name
        })
