from typing import Union, Sequence, List, Dict

import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Output, Input
from dash.development.base_component import Component

from pyfileconfgui.component import PFCGuiComponent
from pyfileconfgui.dash_ext.component import DashPythonComponent
from pyfileconfgui.dash_ext.query import get_triggering_id
from pyfileconfgui.dash_ext.tb import TracebackComponent
from pyfileconfgui.pages.navigator.refresh import is_refresh_trigger, REFRESH_INTERVAL_ID
from pyfileconfgui.pfc.reformat import convert_name_to_id


class ReloadPFCComponent(PFCGuiComponent):
    _should_auto_update: bool = True
    _pm_id_name_map: Dict[str, str]

    def __init__(self, id: str):
        self._pm_id_name_map = {}
        super().__init__(id)

    @property
    def layout(self) -> Sequence[Union[DashPythonComponent, Component]]:
        return [
            *self.buttons,
            html.Div(id='reload-output'),
        ]

    @property
    def buttons(self) -> List[html.Button]:
        buttons = []
        for manager in self.gui.runner.managers.values():
            id_name = convert_name_to_id(manager.name)
            id_ = f'reload-button-{id_name}'
            self._pm_id_name_map[id_] = manager.name
            button = html.Button(f'Reload {manager.name}', id=id_)
            buttons.append(button)

        return buttons

    @property
    def button_ids(self) -> List[str]:
        return [comp.id for comp in self.buttons]

    @property
    def button_inputs(self) -> List[Input]:
        return [Input(id_, 'n_clicks') for id_ in self.button_ids]

    def add_callbacks(self, app: dash.Dash) -> None:
        self.add_callback(
            app,
            self.reload_pfc,
            Output('reload-output', 'children'),
            [*self.button_inputs, Input(REFRESH_INTERVAL_ID, 'n_intervals')]
        )
        super().add_callbacks(app)

    def reload_pfc(self, *args):
        if is_refresh_trigger():
            if self._should_auto_update:
                return ''
            return dash.no_update

        trigger_id = get_triggering_id()
        manager_name = self._pm_id_name_map[trigger_id]
        try:
            self.gui.runner.reload([manager_name])
            self._should_auto_update = True
        except Exception as e:
            self._should_auto_update = False
            return TracebackComponent('reload-pfc-traceback').component
        return f'Reloaded pipeline manager {manager_name}'


