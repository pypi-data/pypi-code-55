from typing import Union, List
from framl.config_model import ConfigModel


class Monitoring:

    def __init__(self, app_path: str):
        model_conf_ob = ConfigModel(app_path)
        self._model_params = model_conf_ob.get_monitored_fields()

        self._model_name = model_conf_ob.get_model_name()
        self._project_id = model_conf_ob.get_gcp_project_id()

    def prepare_table(self) -> None:
        exit("not implemented")

    def list(self) -> dict:
        exit("not implemented")
