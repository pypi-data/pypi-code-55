from abc import ABC
from copy import deepcopy

from dash.dependencies import Output
from dash_html_components import Div

from ..html_helpers.divs import Row
from .callback import Callback


class Component(object):
    def __init__(self, id):
        self.id = id
        self.callbacks = set()

    def find_callbacks(self):
        callbacks = set()
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Callback):
                attr._format(**self.__dict__)
                self.__setattr__(attr.name, attr)
                callbacks.add(attr)

        return callbacks

    def layout(self):
        raise NotImplementedError

    @classmethod
    def from_config(cls, config):
        id = config.get("id")
        if id is None:
            raise AttributeError("No id provided in config")
        component = cls(id)
        for key, value in config.items():
            component.__setattr__(key, value)

        return component

    def _before_registry(self, app):
        self.callbacks = self.find_callbacks()

    def register_callback(self, callback):
        self.callbacks.add(callback)
        return callback


def as_component(dash_object, id, *args, container=None, **kwargs):
    class Wrapper(Component):
        def layout(self):
            if container:
                return container([dash_object(*args, id=id, **kwargs)])
            else:
                return dash_object(*args, id=id, **kwargs)

    return Wrapper(id)
