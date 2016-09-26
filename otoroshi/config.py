# -*- coding: utf-8 -*-
""" Configuration provider for Otoroshi application.
"""

import codecs
from configparser import SafeConfigParser
import os


class Config(object):
    """ This config object provide an abstraction over ConfigParser
    to easily load a configuration from environment variable.
    """
    def __init__(self):
        """ Initialize the config parser object.
        """
        self.parser = SafeConfigParser()

    def from_env(self, variable_name):
        """ Load a configuration file from an environment variable given his
        name.

        Args:
            variable_name (str): Name of the environment variable.

        Raise:
            RuntimeError: If the environment variable is not set.
        """
        value = os.environ.get(variable_name)
        if not value:
            raise RuntimeError('The environment variable %r is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file' %
                               variable_name)

        self.parser.readfp(codecs.open(value, "r", "utf8"))

    def get(self, *args):
        """ Accessor of the get method from ConfigParserObject.

        Return:
            See the `SafeConfigParser.get` documentation.
        """
        return self.parser.get(*args)
