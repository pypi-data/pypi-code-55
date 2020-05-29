import os

from pydmt.api.feature import Feature
from pydmt.builders.sphinx import Sphinx
from pydmt.core.pydmt import PyDMT


class Documentation(Feature):
    def __init__(
        self,
        sphinx_folder: str = "sphinx",
    ):
        self.sphinx_folder = sphinx_folder

    def setup(self, pydmt: PyDMT) -> None:
        if not os.path.isdir(self.sphinx_folder):
            return
        import config.project
        pydmt.add_builder(Sphinx(package_name=config.project.project_name))
