from typing import Union, Sequence

from dash.development.base_component import Component
import dash_core_components as dcc

from pyfileconfgui.dash_ext.component import DashPythonComponent


class PythonBlockComponent(DashPythonComponent):

    def __init__(self, id: str, content: str, **kwargs):
        self.content = content
        super().__init__(id, **kwargs)

    @property
    def layout(self) -> Sequence[Union['DashPythonComponent', Component]]:
        return [
            dcc.Markdown(f'```python\n{self.content}\n```', style={'overflow': 'auto'})
        ]