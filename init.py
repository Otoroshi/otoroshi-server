#!/usr/bin/env python
# -*- coding: utf-8 -*-

from otoroshi.config import Config
from otoroshi.db import Db


if __name__ == '__main__':
    config = Config()
    config.from_env('OTOROSHI_CONFIG')
    database = Db(config)

    print "Creating database ..."
    database.drop_all()
    database.create_all()
    print "Database created"
