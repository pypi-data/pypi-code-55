# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashAntDesignDatePicker(Component):
    """A DashAntDesignDatePicker component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- startDate (string | dict; optional): The begin date.
- endDate (string | dict; optional): The end date."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, startDate=Component.UNDEFINED, endDate=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'startDate', 'endDate']
        self._type = 'DashAntDesignDatePicker'
        self._namespace = 'dash_ant_design_date_picker'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'startDate', 'endDate']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashAntDesignDatePicker, self).__init__(**args)
