# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Stave(Component):
    """A Stave component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- notes (string; required): A label that will be printed when this component is rendered."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, notes=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'notes']
        self._type = 'Stave'
        self._namespace = 'score_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'notes']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['notes']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Stave, self).__init__(**args)
