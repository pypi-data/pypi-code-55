import json
from sentry_sdk import capture_exception
from . import api
from . import data


class Analyzer:
    def __init__(self, queued_analysis_id, converter):
        self.converter = converter
        self.queued_analysis_id = queued_analysis_id

    def test(self):
        queued_analysis = api.get_queued_analysis(self.queued_analysis_id)
        source = api.get_dataset(queued_analysis["source"])
        target_ids = queued_analysis["targets"]
        targets = [api.get_dataset(target_id) for target_id in target_ids]
        source_request = data.get_data_as_stream(source["url"])
        outputs = self.converter(
            source_request=source_request,
            source_settings=source["meta_data"],
            settings=queued_analysis["settings"],
            source=source,
            targets=targets,
        )

        old = data.get_data_as_json(targets[0]["url"])
        new = json.loads(outputs[0]["data"])

        return old == new, old, new

    def start(self):
        self.queued_analysis = api.get_queued_analysis(self.queued_analysis_id)
        self.source = api.get_dataset(self.queued_analysis["source"])
        self.target_ids = self.queued_analysis["targets"]
        self.targets = [api.get_dataset(target_id) for target_id in self.target_ids]
        api.queued_analysis_mark_started(self.queued_analysis_id)
        try:
            source_request = data.get_data_as_stream(self.source["url"])
            outputs = self.converter(
                source_request=source_request,
                source_settings=self.source["meta_data"],
                settings=self.queued_analysis["settings"],
                source=self.source,
                targets=self.targets,
            )
            for target in outputs:
                api.dataset_attach_data(target["id"], target["data"], target["extension"])
        except Exception as e:
            capture_exception(e)
            [api.dataset_abort_upload(target_id) for target_id in self.target_ids]
        api.queued_analysis_mark_ended(self.queued_analysis_id)
