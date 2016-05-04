# -*- coding: utf-8 -*-

import json

from sqlalchemy import Column, Enum, ForeignKey, String  # pylint: disable=F0401
from sqlalchemy.orm import relationship  # pylint: disable=F0401

from otoroshi.db import BaseModel


class Account(BaseModel):  # pylint: disable=R0903,W0232
    __tablename__ = 'accounts'

    username = Column(String(32), primary_key=True, nullable=False)
    secret = Column(String, nullable=False)
    role = Column(
        Enum('admin', 'listener', 'actuator'), nullable=False)

    def __repr__(self):
        return "<Account('%s', '%s')>" % (self.username, self.role)


class Card(BaseModel):  # pylint: disable=R0903,W0232
    __tablename__ = 'cards'

    id = Column(String(32), primary_key=True)  # pylint: disable=C0103
    shortname = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<Card('%s','%s')>" % (self.id, self.fullname)


class Listener(BaseModel):  # pylint: disable=R0903,W0232
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
        return json.dumps({
            "id": self.id,
            "name": self.name
        })


class Actuator(BaseModel):  # pylint: disable=R0903,W0232
    __tablename__ = 'actuators'

    id = Column(String(32), primary_key=True)  # pylint: disable=C0103
    name = Column(String)
    account_username = Column(
        String(32), ForeignKey('accounts.username'), nullable=False)
    account = relationship('Account')

    def __repr__(self):
        return "<Actuator('%s', '%s')>" % (self.id, self.name)

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name
        })
