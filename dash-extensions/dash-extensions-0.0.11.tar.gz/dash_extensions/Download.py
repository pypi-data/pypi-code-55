# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Download(Component):
    """A Download component.
The Download component opens a download dialog when the data property (dict of filename, content, and type) changes.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- data (dict; optional): When set, a download is invoked using a Blob. data has the following type: dict containing keys 'filename', 'content', 'type'.
Those keys have the following types:
  - filename (string; required)
  - content (boolean | number | string | dict | list; required)
  - type (string; required)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data']
        self._type = 'Download'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Download, self).__init__(**args)
