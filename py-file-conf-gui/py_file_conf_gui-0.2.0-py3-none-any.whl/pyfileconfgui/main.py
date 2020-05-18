from typing import Dict, List

from pyfileconf import Selector

from pyfileconfgui.app import create_app
from pyfileconfgui.component import PFCGuiComponent
from pyfileconfgui.index import add_layout
from pyfileconfgui.pfc.extract import full_dict_from_selector
from pyfileconfgui.pfc.reformat import nested_dict_to_paths
from pyfileconfgui.runner import PFCRunner


class PyFileConfGUI:
    structure: dict
    paths: List[str]
    s: Selector

    def __init__(self):
        self.refresh()
        self.runner = PFCRunner()
        self.app = create_app()
        PFCGuiComponent.register_app(self)
        add_layout(self)

    def run_server(self, **kwargs):
        self.app.run_server(**kwargs)

    @property
    def file_objs(self) -> List[Dict[str, str]]:
        return [{'key': path} for path in self.paths]

    def refresh(self):
        self.s = Selector()
        self.structure = full_dict_from_selector(self.s)
        self.paths = nested_dict_to_paths(self.structure)
