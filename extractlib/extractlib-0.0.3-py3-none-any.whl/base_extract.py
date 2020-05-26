import os
import shutil
import pytz
import requests
import boto3
import json
import traceback

from os.path import join
from datetime import datetime
from abc import ABC, abstractmethod
from extractlib.enums import MessageStatus
from extractlib.config_loader import ConfigLoader


class BaseExtract(ABC):
    temp_dir = ".temp"

    @property
    @abstractmethod
    def etl_id(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def namespace(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def data_provider(self):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        assert "env" in kwargs
        self.env_config = ConfigLoader.get_config(kwargs["env"])

    @abstractmethod
    def should_extract(self):
        """User-defined mechanism for short-circuiting out of an extract
            Return False to cancel the extract
        """
        return True

    def get_run(self):
        """Make a POST to Oasis to create a Run object, which tracks the execution of this ETL"""
        data = {
            "etl": self.etl_id,
            "started_by": self.env_config["user_pk"],
            "extract_start": str(datetime.now(pytz.utc)),
        }

        run_endpt = f"{self.env_config['oasis_url']}/data_service/api/v1/runs/"
        headers = {"authorization": self.env_config["auth_token"]}
        return requests.post(run_endpt, json=data, headers=headers).json()["uuid"]

    def emit_event(self, run, event_status, message):
        """Communicate a state change to Oasis by sending an Event object via AWS SNS"""
        event = {
            "event_type": "extract",
            "status": event_status.value,
            "message": message,
            "object_id": self.etl_id.replace("-", ""),
            "run": run.replace("-", ""),
            "content_type": "etl",
        }

        self.sns.publish(
            TopicArn=self.env_config["event_queue_arn"], Message=json.dumps(event)
        )

    def upload(self):
        """Upload the data to S3 in preparation for transform"""
        s3 = boto3.client("s3")
        bucket = self.env_config["upload_bucket"]
        now = datetime.now()
        path = "/".join(
            [
                self.env_config["env_code"],
                "data_provider=" + self.data_provider,
                "namespace=" + self.namespace,
                "year=" + now.strftime("%Y"),
                "month=" + now.strftime("%m"),
                "day=" + now.strftime("%d"),
            ]
        )
        for root, dirs, files in os.walk(self.temp_dir):
            for tmpfile in files:
                s3.upload_file(
                    join(self.temp_dir, tmpfile), bucket, join(path, tmpfile)
                )
        self.upload_path_dict = {
            "data_location": "s3a://" + bucket + "/" + path,
            "input_name": "Default Input",
        }

    def set_inputs(self):
        """Set the inputs for the spark job. 
            By default, uses the path to which files are uploaded.
            To use another path, overwrite in the specific extract
        """
        self.inputs = [self.upload_path_dict]

    def cleanup(self):
        """Delete the local data directory"""
        shutil.rmtree(self.temp_dir)

    def create_spark_message(self, run):
        """Create the spark message needed to kick off a transform job"""
        run_message_body = {}
        spark_config_keys = {
            "spark_driver_cores",
            "spark_driver_memory",
            "spark_executor_cores",
            "spark_executor_memory",
            "spark_num_executors",
            "spark_queue",
        }

        for key in spark_config_keys:
            run_message_body[key] = self.env_config[key]
        run_message_body["etl"] = self.etl_id
        run_message_body["run"] = run
        run_message_body["args"] = ["--namespace", self.namespace, "--run-uuid", run]
        run_message_body["file"] = self.env_config["jar_file"]
        run_message_body["applied_data_inputs"] = []
        for input_dict in self.inputs:
            run_message_body["applied_data_inputs"].append(
                {
                    "data_location": input_dict["data_location"],
                    "input_name": input_dict["input_name"],
                }
            )
        self.run_message_body = run_message_body

    def submit_spark_message(self):
        """Post spark message to Oasis"""
        header = {
            "Accept": "application/json, application/json",
            "Content-Type": "application/json",
            "Authorization": self.env_config["auth_token"],
        }
        requests.post(
            self.env_config["start_spark_url"],
            headers=header,
            json=self.run_message_body,
        )

    @abstractmethod
    def preprocess(self, data_dir):
        """User-defined method for pre-transform data manipulation
           The user is responsible for manipulating the file(s) in the local storage directory.
           The contents of that directory will be used as input for the transform step
        """
        raise NotImplementedError

    @abstractmethod
    def fetch(self):
        """fetches the data"""
        raise NotImplementedError

    def extract(self):
        """The main function executes an extract from end to end"""
        self.sns = boto3.client("sns")
        if self.should_extract():
            run = self.get_run()
            try:
                if not os.path.exists(self.temp_dir):
                    os.makedirs(self.temp_dir)
                self.fetch()
                self.preprocess(data_dir=self.temp_dir)
                self.upload()
                self.set_inputs()
                self.create_spark_message(run)
                self.submit_spark_message()
                self.emit_event(run, MessageStatus.SUCCESS, "Ready for Transfrom")
            except Exception as ex:
                self.emit_event(run, MessageStatus.ERROR, traceback.format_exc())
            finally:
                self.cleanup()
