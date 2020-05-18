import time
from queue import Queue
from typing import List

from framl.config_model import ConfigModel
from google.cloud import logging
from google.cloud.logging.resource import Resource


class Logger:
    MESSAGE_VERSION = 1
    BUFFER_TIME = 60

    def __init__(self, app_path: str):
        model_conf_ob = ConfigModel(app_path)

        self._model_name = model_conf_ob.get_model_name()
        self._model_version = model_conf_ob.get_model_version()
        self._logs_buffer = Queue()
        self._last_flush_time = time.time()

        logging_client = logging.Client(project=model_conf_ob.get_gcp_project_id())
        self.sd_logger = logging_client.logger("framl.blablacar.com%2F" + self._model_name.replace("-", "_"))

        self.log_res = Resource(
            type="api",
            labels={
                "project_id": model_conf_ob.get_gcp_project_id(),
                "service":    self._model_name,
                "method":     "/predict",
                "version":    str(model_conf_ob.get_model_version()),
                "location":   "global"
            },
        )

    def flush_logs(self):
        logs = []
        for _ in range(self._logs_buffer.qsize()):
            logs.append(self._logs_buffer.get())

        with self.sd_logger.batch() as batch:
            for m in logs:
                batch.log_struct(m, resource=self.log_res)

    def add(self, prediction_id: str, model_input: dict, model_output: dict, latency: int):
        full_log = {
            "request_latency_in_ms": latency,
            "prediction_id":         prediction_id,
            "message_version":       self.MESSAGE_VERSION,
            "prediction_time":       int(time.time()),
            "metadata":              {
                "model_name":    self._model_name,
                "model_version": self._model_version,
            },
            "input":                 {**model_input},
            "output":                {**model_output}
        }

        self._logs_buffer.put_nowait(full_log)
        if self._last_flush_time + Logger.BUFFER_TIME <= time.time():
            self._last_flush_time = time.time()
            self.flush_logs()

    def add_batch(self, prediction_id: str, model_inputs: List[dict], model_outputs: List[dict], latency: int):

        if len(model_inputs) != len(model_outputs):
            raise Exception("model input/ouput are not matching. Logging impossible")

        for i, input in enumerate(model_inputs):
            self.add(prediction_id, input, model_outputs[i], latency)