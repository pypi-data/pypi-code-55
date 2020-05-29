import hashlib
import os
import re
from pathlib import Path
from typing import Dict

from ruamel.yaml import YAML

from cognite.client.data_classes import Event
from cognite.client.experimental import CogniteClient


class Utils:
    @classmethod
    def _path_to_function_dir(cls) -> Path:
        function_dir = Path(os.getcwd())
        while function_dir.parts[-1] != "function":
            function_dir = function_dir.parent
        return function_dir

    @classmethod
    def _read_init(cls) -> str:
        init_path = cls._path_to_function_dir() / "__init__.py"
        with init_path.open(mode="r") as init:
            init_content = init.read()
        return init_content

    @classmethod
    def retrieve_version(cls) -> str:
        init = cls._read_init()
        version = init.split("\n")[0].split(" = ")[1]
        version = re.sub('"', "", version)
        version = ".".join(version.split(".")[:-1])
        return version

    @classmethod
    def retrieve_model_name(cls) -> str:
        init = cls._read_init()
        model_name = init.split("\n")[1].split(" = ")[1]
        model_name = re.sub('"', "", model_name)
        return model_name

    @staticmethod
    def read_yaml(file: str) -> Dict:
        yaml_file = YAML(typ="safe").load(file)
        return yaml_file

    @staticmethod
    def retrieve_data_set_id(client: CogniteClient) -> int:
        data_sets_id = client.data_sets.list(limit=-1).to_pandas().query('name == "AIR"').id.iloc[0]
        return data_sets_id

    @classmethod
    def retrieve_project_name(cls) -> str:
        return os.environ["COGNITE_PROJECT"]

    @classmethod
    def create_event(
        cls, ts_id: int, ts_external_id: str, start: int, end: int, client: CogniteClient, metadata: Dict = None
    ) -> Event:

        if metadata is None:
            metadata = {}
        metadata.update(
            {
                "model": cls.retrieve_model_name(),
                "model_asset_id": str(cls.retrieve_model_asset_id(client)),
                "model_version": cls.retrieve_version(),
                "time_series_id": str(ts_id),
                "time_series_external_id": ts_external_id,
                "description": cls.retrieve_model_description(client),
                "type_of_event": cls.retrieve_clean_model_name(client),
            }
        )

        event_external_id = cls.create_event_external_id(
            ts_external_id, cls.retrieve_model_name(), cls.retrieve_version(), start, end
        )

        if client.events.retrieve(external_id=event_external_id):
            return Event()

        model_output_event = Event(
            external_id=event_external_id,
            start_time=start,
            end_time=end,
            data_set_id=cls.retrieve_data_set_id(client),
            type="AIR",
            subtype="model_output",
            metadata=metadata,
        )
        client.events.create(model_output_event)
        return model_output_event

    @classmethod
    def retrieve_schedule_config(cls, client: CogniteClient) -> Dict:
        model_name = cls.retrieve_model_name()
        model_asset = client.assets.list(data_set_ids=cls.retrieve_data_set_id(client), name=model_name)[0].dump()
        return model_asset

    @classmethod
    def retrieve_model_description(cls, client: CogniteClient) -> str:
        schedule_config = cls.retrieve_schedule_config(client)
        description = schedule_config.get("description")
        return description if description else ""

    @classmethod
    def retrieve_clean_model_name(cls, client: CogniteClient) -> str:
        schedule_config = cls.retrieve_schedule_config(client)
        metadata = schedule_config.get("metadata")
        if metadata:
            return metadata.get("frontEndName")
        return ""

    @classmethod
    def retrieve_model_asset_id(cls, client: CogniteClient) -> int:
        model_name = cls.retrieve_model_name()
        assets = client.assets.list(name=model_name, data_set_ids=[cls.retrieve_data_set_id(client)])
        asset_id = assets[0].id
        return asset_id

    @staticmethod
    def create_event_external_id(
        ts_external_id: str, model_name: str, model_version: str, start_time: int, end_time: int
    ) -> str:

        to_be_hashed = model_name + model_version + ts_external_id + str(start_time) + str(end_time)
        hash_object = hashlib.md5(to_be_hashed.encode())
        return hash_object.hexdigest()

    @classmethod
    def retrieve_dependency(cls, model_name: str) -> str:
        path = cls._path_to_function_dir() / "resources/dependencies.yaml"
        dependency = cls.read_yaml(str(path)).get(model_name)
        return dependency if dependency else ""

    @classmethod
    def retrieve_window_size(cls, client: CogniteClient) -> int:
        asset_id = cls.retrieve_model_asset_id(client)
        schedule = eval(client.assets.retrieve(asset_id).metadata.get("schedule"))
        if schedule.get("windowSize"):
            return int(schedule.get("windowSize"))
        return 0
