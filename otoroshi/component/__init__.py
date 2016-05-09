# -*- coding: utf-8 -*-
""" The component package provide components that expose some functionnality
like authorization, management or all the features exposed to the Otoroshi
network.
"""


class Component(object):  # pylint: disable=R0903
    """ Base class of Otoroshi components, components are set to expose the
    rpc and pubsub methods. This base class first goal is to expose the
    application to provide settings, db access and lot more.
    """
    REGISTER_OPTIONS = None

    def __init__(self, app):
        """ When the component is constructed, some private properties
        are created to ease the component developpment. For example, it
        expose the app context and the database session object.

        Args:
            app (otoroshi.OtoroshiSession): The Otoroshi application session.
        """
        self._app = app
        self._session = self._app.database.session
