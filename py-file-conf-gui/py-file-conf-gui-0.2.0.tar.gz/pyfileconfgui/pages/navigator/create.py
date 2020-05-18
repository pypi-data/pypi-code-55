import importlib
import traceback
from typing import Union, Sequence, Optional

import dash
from dash.dependencies import Output, Input, State
from dash.development.base_component import Component
import dash_core_components as dcc
import dash_html_components as html
from pyfileconf.imports.models.statements.obj import ObjectImportStatement

from pyfileconfgui.component import PFCGuiComponent
from pyfileconfgui.dash_ext.component import DashPythonComponent
from pyfileconfgui.dash_ext.tb import TracebackComponent


class CreateEntryComponent(PFCGuiComponent):

    @property
    def layout(self) -> Sequence[Union['DashPythonComponent', Component]]:
        layout = [
            html.H3('Create Item'),
            html.Label('Section Path'),
            dcc.Input(id='section-path-input', placeholder='my.section.path', value=''),
            html.Label('Function/Class Import  (optional)'),
            dcc.Input(id='function-class-import-input', placeholder='from mymod import Stuff', value=''),
            html.Button('Submit', id='create-item-submit-button'),
            html.Div(id='create-item-output')
        ]

        return layout

    def add_callbacks(self, app: dash.Dash) -> None:
        self.add_callback(
            app,
            self.create_item,
            Output('create-item-output', 'children'),
            [Input('create-item-submit-button', 'n_clicks')],
            (State('section-path-input', 'value'), State('function-class-import-input', 'value'))
        )
        super().add_callbacks(app)

    def create_item(self, n_clicks: int, section_path: str, function_class_import: Optional[str]):
        try:
            return self._create_item(n_clicks, section_path, function_class_import)
        except Exception as e:
            return TracebackComponent('create-item-tb').component

    def _create_item(self, n_clicks: int, section_path: str, function_class_import: Optional[str]):
        if not section_path:
            return dash.no_update
        if function_class_import:
            imp = ObjectImportStatement.from_str(function_class_import)
            if len(imp.objs) != 1:
                raise ValueError(f'must have exactly one object import, got {imp.objs}')
            mod = importlib.import_module(imp.module)
            func_or_class = getattr(mod, imp.objs[0])
        else:
            func_or_class = None
        output = self.gui.runner.create(section_path, func_or_class)
        return f'Created {section_path}'
