import traceback
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
from pyfileconfgui.dash_ext.python import PythonBlockComponent
from pyfileconfgui.dash_ext.tb import TracebackComponent


class RunEntryComponent(PFCGuiComponent):
    is_running: bool = False
    log_buffer: StringIO = StringIO()

    @property
    def layout(self) -> Sequence[Union['DashPythonComponent', Component]]:
        return [
            html.H2('Running Item'),
            html.P(id='run-input'),
            html.Div(id='run-console-output'),
            dcc.Loading(html.Div(id='run-output')),
            dcc.Interval('run-poll-interval', 500, disabled=True),
        ]

    def add_callbacks(self, app: dash.Dash) -> None:
        from pyfileconfgui.pages.navigator.refresh import REFRESH_INTERVAL_ID
        self.add_callback(
            app,
            self.run_item,
            Output('run-output', 'children'),
            [Input('run-input', 'children')]
        )
        self.add_callback(
            app,
            self.set_polling,
            Output('run-poll-interval', 'disabled'),
            [Input('run-input', 'children'), Input(REFRESH_INTERVAL_ID, 'n_intervals')]
        )
        self.add_callback(
            app,
            self.stream_output,
            Output('run-console-output', 'children'),
            [Input('run-poll-interval', 'n_intervals'), Input(REFRESH_INTERVAL_ID, 'n_intervals')]
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
        try:
            output = self.gui.runner.run(path)
        except Exception as e:
            sys.stdout = orig_stdout
            self.is_running = False
            return TracebackComponent('run-output-tb').component
        sys.stdout = orig_stdout
        self.is_running = False
        return str(output)

    def set_polling(self, path: str, n_check_intervals: int):
        # Sets disabled for poll interval
        if self.is_running:
            # is running, poll should not be disabled
            return False
        # not running, poll should be disabled
        return True

    def stream_output(self, n_poll_intervals: int, n_check_intervals: int):
        return PythonBlockComponent('run-output-python-block', self.log_output).component

    def reset_log(self):
        self.log_buffer.truncate(0)
        self.log_buffer.seek(0)
