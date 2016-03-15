# -*- coding: utf-8 -*-


from sqlalchemy import Column, String
from .db import BaseModel


class Card(BaseModel):
    __tablename__ = 'cards'

    id = Column(String(32), primary_key=True)
    shortname = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<Card('%s','%s')>" % (self.id, self.fullname)
