from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from pyfileconfgui.main import PyFileConfGUI

from pyfileconfgui.dash_ext.component import DashPythonComponent


class PFCGuiComponent(DashPythonComponent):
    gui: 'PyFileConfGUI'

    @classmethod
    def register_app(cls, gui: 'PyFileConfGUI'):
        cls.gui = gui
        super().register_app(gui.app)
