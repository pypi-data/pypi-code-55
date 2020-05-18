from typing import Type, Sequence, Union, Optional, List, Callable

import dash
from dash.dependencies import Output, Input, State
from dash.development.base_component import Component
import dash_html_components as html


class DashPythonComponent:
    app: Optional[dash.Dash] = None
    _callback_output_ids: List[str] = []

    def __init__(self, id: str, **kwargs):
        self.id = id
        self.component_kwargs = kwargs

        if self.app is not None:
            self.add_callbacks(self.app)

    @property
    def component(self) -> html.Div:
        layout = self.layout
        dash_layout = []
        for comp in layout:
            if isinstance(comp, DashPythonComponent):
                dash_comp = comp.component
            else:
                dash_comp = comp
            dash_layout.append(dash_comp)
        return html.Div(dash_layout, id=self.id, **self.component_kwargs)

    @property
    def layout(self) -> Sequence[Union['DashPythonComponent', Component]]:
        raise NotImplementedError

    @classmethod
    def register_app(cls, app: dash.Dash):
        cls.app = app

    def add_callbacks(self, app: dash.Dash) -> None:
        layout = self.layout
        for comp in layout:
            if isinstance(comp, DashPythonComponent):
                comp.add_callbacks(app)

    def add_callback(self, app: dash.Dash, func: Callable, output: Output, inputs: Sequence[Input],
                     state: Sequence[State] = tuple(), prevent_initial_call: Optional[bool] = None) -> None:
        if output.component_id in self._callback_output_ids:
            return
        self._callback_output_ids.append(output.component_id)
        app.callback(output, inputs, state, prevent_initial_call=prevent_initial_call)(func)
