import traceback

from pyfileconfgui.dash_ext.python import PythonBlockComponent

DEFAULT_HEIGHT = '300px'


class TracebackComponent(PythonBlockComponent):

    def __init__(self, id: str, **kwargs):
        if 'style' not in kwargs:
            kwargs['style'] = {'max-height': DEFAULT_HEIGHT}
        elif 'max-height' not in kwargs['style']:
            kwargs['style']['max-height'] = DEFAULT_HEIGHT
        content = traceback.format_exc()
        super().__init__(id, content, **kwargs)

    def refresh(self):
        self.content = traceback.format_exc()
