#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid

from otoroshi.config import Config
from otoroshi.db import Db
from otoroshi.model import Account, Actuator, Card, Listener


if __name__ == '__main__':
    config = Config()
    config.from_env('OTOROSHI_CONFIG')
    database = Db(config)

    print "Creating database ..."
    database.drop_all()
    database.create_all()

    accounts = (
        ("admin", "admin", "admin"),
        ("listener", "listener", "listener"),
        ("actuator", "actuator", "actuator"),
    )

    for i, account in enumerate(accounts):
        database.session.add(Account(
            username=account[0],
            secret=account[1],
            role=account[2]
        ))
        database.session.commit()

    actuators = (
        ("actuator_1", "1", "actuator"),
    )
    for i, actuator in enumerate(actuators):
        database.session.add(Actuator(
            id=actuator[0],
            name=actuator[1],
            account_username=actuator[2]
        ))
        database.session.commit()

    listeners = (
        (str(uuid.uuid4()), "listener_1", "actuator_1", "listener", "1"),
    )
    for i, listener in enumerate(listeners):
        database.session.add(Listener(
            id=listener[0],
            name=listener[1],
            actuator_id=listener[2],
            account_username=listener[3],
            actuator_channel=listener[4],
        ))
        database.session.commit()

    cards = (
        ("card_1", "Romain", "Vorex"),
    )
    for i, card in enumerate(cards):
        database.session.add(Card(
            id=card[0],
            shortname=card[1],
            fullname=card[2]
        ))
        database.session.commit()

    print "Database created"
