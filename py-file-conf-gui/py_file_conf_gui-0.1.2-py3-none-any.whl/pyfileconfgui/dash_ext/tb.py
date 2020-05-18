import traceback

from pyfileconfgui.dash_ext.python import PythonBlockComponent


class TracebackComponent(PythonBlockComponent):

    def __init__(self, id: str):
        content = traceback.format_exc()
        super().__init__(id, content)

    def refresh(self):
        self.content = traceback.format_exc()
