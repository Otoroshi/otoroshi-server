# -*- coding: utf-8 -*-
import json
from sqlalchemy import Column, String
from .db import BaseModel


class Card(BaseModel):
    __tablename__ = 'cards'

    id = Column(String(32), primary_key=True)
    shortname = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<Card('%s','%s')>" % (self.id, self.fullname)


class Listener(BaseModel):
    __tablename__ = 'listeners'

    id = Column(String(32), primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Listener('%s', '%s')>" % (self.id, self.name)

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name
        })
