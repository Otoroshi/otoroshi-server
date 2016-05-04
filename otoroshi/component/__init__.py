# -*- coding: utf-8 -*-


class Component(object):
    """ Base class of Otoroshi components, components are set to expose the
    rpc and pubsub methods. This base class first goal is to expose the
    application to provide settings, db access and lot more.
    """
    _REGISTER_OPTIONS = None

    def __init__(self, app):
        self._app = app
        self._session = self._app.database.session
