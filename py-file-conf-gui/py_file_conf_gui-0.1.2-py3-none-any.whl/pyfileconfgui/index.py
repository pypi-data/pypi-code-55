from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyfileconfgui.main import PyFileConfGUI

from pyfileconfgui.component import PFCGuiComponent
from pyfileconfgui.dash_ext.router import RouterComponent
from pyfileconfgui.pages.navigator.main import NavigatorComponent


class PFCGUIRouterComponent(PFCGuiComponent, RouterComponent):
    pass


def add_layout(gui: 'PyFileConfGUI'):
    app = gui.app

    nav_component = NavigatorComponent('navigator-root')

    routes = {
        '/': nav_component,
        '/navigator': nav_component
    }

    layout_component = PFCGUIRouterComponent('layout-root', routes)

    app.layout = layout_component.component
    app.validation_layout = layout_component.validation_component

