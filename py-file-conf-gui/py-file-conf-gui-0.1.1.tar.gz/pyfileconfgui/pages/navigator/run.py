import time
from io import StringIO
from typing import Union, Sequence
import sys

import dash
from dash.dependencies import Output, Input
from dash.development.base_component import Component
import dash_core_components as dcc
import dash_html_components as html

from pyfileconfgui.component import PFCGuiComponent
from pyfileconfgui.dash_ext.component import DashPythonComponent


class RunEntryComponent(PFCGuiComponent):
    is_running: bool = False
    log_buffer: StringIO = StringIO()

    @property
    def layout(self) -> Sequence[Union['DashPythonComponent', Component]]:
        return [
            html.H2('Running Item'),
            html.P(id='run-input'),
            html.Div(id='run-interval-container'),
            html.Div(id='run-console-output'),
            html.Div(id='run-output'),
        ]

    def add_callbacks(self, app: dash.Dash) -> None:
        self.add_callback(
            app,
            self.run_item,
            Output('run-output', 'children'),
            [Input('run-input', 'children')]
        )
        self.add_callback(
            app,
            self.set_polling,
            Output('run-interval-container', 'children'),
            [Input('run-input', 'children'), Input('run-console-output', 'children')]
        )
        self.add_callback(
            app,
            self.stream_output,
            Output('run-console-output', 'children'),
            [Input('run-interval', 'n_intervals')]
        )
        super().add_callbacks(app)

    @property
    def log_output(self) -> str:
        return self.log_buffer.getvalue()

    def run_item(self, path: str):
        self.reset_log()
        self.is_running = True
        orig_stdout = sys.stdout
        sys.stdout = self.log_buffer
        output = self.gui.runner.run(path)
        # TODO [#2]: run item gets stuck polling if run finishes too fast
        #
        # For now, just sleeping the same amount as the interval to ensure
        # that the interval happens at least once. Tried hooking stop interval
        # to final output but didn't work.
        time.sleep(0.5)
        sys.stdout = orig_stdout
        self.is_running = False
        return str(output)

    def set_polling(self, path: str, run_output: str):
        if self.is_running:
            return dcc.Interval('run-interval', 500)
        return None

    def stream_output(self, n_intervals: int):
        return dcc.Markdown(f'```python\n{self.log_output}\n```', style={'overflow': 'auto'})

    def reset_log(self):
        self.log_buffer.truncate(0)
        self.log_buffer.seek(0)
