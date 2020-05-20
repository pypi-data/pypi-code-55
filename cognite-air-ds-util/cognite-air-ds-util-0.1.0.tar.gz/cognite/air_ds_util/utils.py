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
    def _path_to_this_file(cls) -> Path:
        this_dir = Path(os.path.abspath(__file__)).parent
        return this_dir

    @classmethod
    def retrieve_version(cls) -> str:
        init_path = cls._path_to_this_file().parent / "__init__.py"
        with init_path.open(mode="r") as init:
            version = init.read().split("\n")[0].split(" = ")[1]
        version = re.sub('"', "", version)
        version = ".".join(version.split(".")[:-1])
        return version

    @staticmethod
    def read_yaml(file: str) -> Dict:
        yaml_file = YAML(typ="safe").load(file)
        return yaml_file

    @classmethod
    def retrieve_model_name(cls) -> str:
        this_dir = cls._path_to_this_file()
        return this_dir.parent.parent.parts[-1]

    @staticmethod
    def retrieve_data_set_id(client: CogniteClient) -> int:
        data_sets_df = client.data_sets.list(limit=-1).to_pandas()
        return data_sets_df.loc[data_sets_df["name"] == "AIR", "id"].iloc[0]

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
                "model": Utils.retrieve_model_name(),
                "model_asset_id": str(Utils.retrieve_model_asset_id(client)),
                "model_version": Utils.retrieve_version(),
                "time_series_id": str(ts_id),
                "time_series_external_id": ts_external_id,
                "description": Utils.retrieve_model_description(client),
                "type_of_event": Utils.retrieve_clean_model_name(client),
            }
        )

        event_external_id = Utils.create_event_external_id(
            ts_external_id, Utils.retrieve_model_name(), Utils.retrieve_version(), start, end
        )

        if client.events.retrieve(external_id=event_external_id):
            return Event()

        model_output_event = Event(
            external_id=event_external_id,
            start_time=start,
            end_time=end,
            data_set_id=Utils.retrieve_data_set_id(client),
            type="AIR",
            subtype="model_output",
            metadata=metadata,
        )
        client.events.create(model_output_event)
        return model_output_event

    @classmethod
    def retrieve_schedule_config(cls, client: CogniteClient) -> Dict:
        model_name = cls.retrieve_model_name()
        model_asset = client.assets.list(data_set_ids=Utils.retrieve_data_set_id(client), name=model_name)[0].dump()
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
        asset_id = client.assets.list(name=model_name, data_set_ids=cls.retrieve_data_set_id(client))[0].id
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
        path = cls._path_to_this_file().parent / "resources/dependencies.yaml"
        dependency = Utils.read_yaml(str(path)).get(model_name)
        return dependency if dependency else ""
