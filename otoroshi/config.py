# -*- coding: utf-8 -*-

import codecs
from ConfigParser import SafeConfigParser
import os


class Config(object):
    def __init__(self):
        self.parser = SafeConfigParser()

    def from_env(self, variable_name):
        value = os.environ.get(variable_name)
        if not value:
            raise RuntimeError('The environment variable %r is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file' %
                               variable_name)

        self.parser.readfp(codecs.open(value, "r", "utf8"))

    def get(self, *args):
        return self.parser.get(*args)
