from pyfileconf import Selector

from pyfileconfgui import PyFileConfGUI
from tests.pfc import full_pm_setup

if __name__ == '__main__':
    pm = full_pm_setup()
    gui = PyFileConfGUI()
    gui.run_server(debug=True, use_reloader=False)