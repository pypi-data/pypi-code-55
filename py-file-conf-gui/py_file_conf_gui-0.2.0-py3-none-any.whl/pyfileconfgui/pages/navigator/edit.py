from typing import Union, Sequence

import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Output, Input
from dash.development.base_component import Component

from pyfileconfgui.component import PFCGuiComponent
from pyfileconfgui.dash_ext.component import DashPythonComponent


def edit_item(path: str):
    # TODO [#1]: read file and instantiate editor
    return path


class EditItemComponent(PFCGuiComponent):

    @property
    def layout(self) -> Sequence[Union[DashPythonComponent, Component]]:
        return [
            html.H2('Edit Item'),
            html.P(id='edit-item-name-output'),
            html.Div(id='editor-output'),
        ]

    def add_callbacks(self, app: dash.Dash) -> None:
        self.add_callback(
            app,
            edit_item,
            Output('editor-output', 'children'),
            [Input('edit-item-name-output', 'children')]
        )
        super().add_callbacks(app)
