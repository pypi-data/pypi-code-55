from typing import TYPE_CHECKING, Dict, Union, Sequence

from dash.dependencies import Output, Input
from dash.development.base_component import Component

from pyfileconfgui.component import PFCGuiComponent
from pyfileconfgui.dash_ext.component import DashPythonComponent
from pyfileconfgui.pages.navigator.create import CreateEntryComponent
from pyfileconfgui.pages.navigator.edit import EditItemComponent
from pyfileconfgui.pages.navigator.refresh import REFRESH_INTERVAL_ID
from pyfileconfgui.pages.navigator.reload import ReloadPFCComponent
from pyfileconfgui.pages.navigator.run import RunEntryComponent


import dash_core_components as dcc
import dash_html_components as html
from dash_keyed_file_browser import KeyedFileBrowser
from dash import dash


def show_running_item(selected_file: Dict[str, str]):
    if not selected_file:
        return dash.no_update
    path = selected_file['key']
    return path


def show_editing_item(selected_file: Dict[str, str]):
    if not selected_file:
        return dash.no_update
    path = selected_file['key']
    return path


class NavigatorComponent(PFCGuiComponent):

    @property
    def layout(self) -> Sequence[Union['DashPythonComponent', Component]]:
        app = self.gui.app

        layout = [
            html.Label('Pyfileconf Items'),
            dcc.Interval(REFRESH_INTERVAL_ID, 2000),
            ReloadPFCComponent('reload-pfc-root'),
            KeyedFileBrowser(self.gui.file_objs, id='kfb'),
            CreateEntryComponent('create-item-root'),
            RunEntryComponent('run-item-root'),
            EditItemComponent('edit-item-root'),
        ]

        return layout

    def add_callbacks(self, app: dash.Dash) -> None:
        self.add_callback(
            app,
            show_running_item,
            Output('run-input', 'children'),
            [Input('kfb', 'openFile')]
        )
        self.add_callback(
            app,
            self.update_files_after_creating_item,
            Output('kfb', 'files'),
            [Input('create-item-output', 'children')]
        )
        self.add_callback(
            app,
            show_editing_item,
            Output('edit-item-name-output', 'children'),
            [Input('kfb', 'selectedFile')]
        )
        super().add_callbacks(app)

    def update_files_after_creating_item(self, updated_message: str):
        self.gui.refresh()
        return self.gui.file_objs



