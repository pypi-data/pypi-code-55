import os
import tempfile

from pip._vendor import requests

from .base_template_store import BaseTemplateStore
from . import template_store_mappings


class SimpleTemplateStore(BaseTemplateStore):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_store_url = kwargs["template_store_url"]

    def get_template(self, template_name: str):
        if template_store_mappings.get(template_name):
            template_url = os.path.join(self.template_store_url, template_store_mappings.get(template_name))
            template_file_path = self._download_to(url=template_url, file_name=template_name)
            return template_file_path
        return None

    def _download_to(self, *, url, file_name):
        response = requests.get(url, params={"raw": True})
        directory = os.path.join(tempfile.gettempdir(), "bricksdk")
        if not os.path.exists(directory):
            os.mkdir(directory)
        file_path = os.path.join(directory, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
