# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashReactWordcloud(Component):
    """A DashReactWordcloud component.
Wordcloud is used to render a cloud of words using the react-wordcloud component
by chrisrzhou:
https://github.com/chrisrzhou/react-wordcloud

Keyword arguments:
- words (list; required): An array of words.
A word is an object that must contain the ‘text’ and ‘value’ keys.
- id (string; optional): The ID used to identify this component in Dash callbacks.
- maxWords (number; optional): Maximum number of words to display
- minSize (list; optional): Set minimum [width, height] values for the SVG container.
- size (list; optional): Set explicit [width, height] values for the SVG container.
This will disable responsive resizing.
If undefined, the wordcloud will responsively size to its parent container.
- options (dict; optional): Configure the wordcloud with various options.
- clickedWord (dict; optional): Word that has been clicked"""
    @_explicitize_args
    def __init__(self, words=Component.REQUIRED, id=Component.UNDEFINED, maxWords=Component.UNDEFINED, minSize=Component.UNDEFINED, size=Component.UNDEFINED, options=Component.UNDEFINED, clickedWord=Component.UNDEFINED, **kwargs):
        self._prop_names = ['words', 'id', 'maxWords', 'minSize', 'size', 'options', 'clickedWord']
        self._type = 'DashReactWordcloud'
        self._namespace = 'dash_react_wordcloud'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['words', 'id', 'maxWords', 'minSize', 'size', 'options', 'clickedWord']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['words']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashReactWordcloud, self).__init__(**args)
