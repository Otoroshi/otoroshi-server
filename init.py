#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otoroshi.config import Config
from otoroshi.db import Db
from otoroshi.model import Account


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
        ("actuator", "actuator", "actuator_manager"),
    )

    for i, account in enumerate(accounts):
        database.session.add(Account(
            username=account[0],
            secret=account[1],
            role=account[2]
        ))
        database.session.commit()
    print "Database created"
