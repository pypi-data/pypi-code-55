from copy import deepcopy
from typing import Dict

from dash import Dash
from dash_bootstrap_components import Alert
from dash_bootstrap_components.themes import BOOTSTRAP
from dash_core_components import Markdown
from dash_html_components import H5, H6, Button, Div
from markdown2 import markdown

from ..components import ComponentGroup
from ..html_helpers.divs import Container, Row, Col
from . import as_component, as_callback


class KWSDashApp:
    def __init__(self, name="Default Dash App", doc=""):
        self.name = name
        self.components = []
        self.component_layouts = []
        self.callbacks = set()
        self.doc = doc
        self.md_doc = markdown(doc)
        self.registered_components = set()
        self.create_header()

    def create_header(self):
        self.component_layouts.append(
            ComponentGroup(
                "header",
                as_component(H5, "app-title", self.name, container=Row),
                as_component(
                    Button,
                    id="show-doc",
                    children="Voir la documentation",
                    className="btn-flat blue lighten-5 btn-small",
                    container=Row,
                ),
                container=Div,
            ).layout()
        )

        self.component_layouts.append(
            as_component(
                Alert,
                f"{self.name}-app-description",
                Markdown(self.doc),
                color="info",
                dismissable=True,
                is_open=False
            ).layout()
        )

        self.callbacks.add(
            as_callback(
                inputs=[("show-doc", "n_clicks")],
                outputs=(f"{self.name}-app-description", "is_open"),
                states=[(f"{self.name}-app-description", "is_open")],
            )(self._show_doc)
        )

    def _show_doc(self, n_click, is_open):
        if n_click:
            return not is_open
        return is_open

    def register_component(self, component):
        if component.id not in self.registered_components:
            self.components.append(component)

    def _register_component(self, group_or_component, app, top=True):
        self.registered_components.add(group_or_component.id)
        group_or_component._before_registry(app)
        if top:
            self.component_layouts.append(group_or_component.layout())

        for callback in group_or_component.callbacks:
            self.callbacks.add(callback)

        if isinstance(group_or_component, ComponentGroup):
            for component in group_or_component.components:
                self._register_component(component, app, top=False)

    def register_callback(self, callback, outputs=None, inputs=None, states=None):
        callback.register(outputs, inputs, states)
        self.callbacks.add(callback)
        return callback

    def instanciate(self, *args, **kwargs):
        app = Dash(
            __name__,
            *args,
            **kwargs,
            suppress_callback_exceptions=True,
            external_stylesheets=[
                BOOTSTRAP,
                "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css",
            ],
            external_scripts=[
                "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js",
            ],
        )

        for component in self.components:
            self._register_component(component, app)

        for callback in self.callbacks:
            if callback.dash_outputs:

                app.callback(
                    callback.dash_outputs, callback.dash_inputs, callback.dash_states
                )(callback.run)

        app.layout = Container(self.component_layouts, id=f"main-div")

        return app

    def run_server(self, *args, **kwargs):
        return self.instanciate().run_server(*args, **kwargs)
