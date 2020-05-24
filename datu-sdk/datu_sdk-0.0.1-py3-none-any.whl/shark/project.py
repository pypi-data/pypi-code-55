"""Model definition for component of the Datu API.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, List, Union
import json
import os
import typing

import jsonpickle
import tabulate

from .annotation_task import AnnotationTask
from .common.enums import (
    TaskType, SamplingStrategy, RequestType, RouteType)
from .common.logging import logger
from .trainer import Trainer
from .base_api import BaseAPI


JSONTYPE = Dict[str, Union[str, List[TaskType]]]


class Sample():
    """A sample of the data.
    """

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return "<Sample name='%s'" % self.name


class Project(BaseAPI):
    """A Datu project.
    """

    project_name: str
    project_id: str
    task_list: List[TaskType]

    def populate_from_json(self, json_data: JSONTYPE) -> None:
        """Populate the instance from the json.
        """
        required_fields = set(['project_name', 'project_id', 'task_list'])
        missing_keys = required_fields - set(json_data.keys())

        if missing_keys:
            logger.error('Required fields are missing: %s', str(missing_keys))
            return

        assert isinstance(json_data['project_name'], str)
        self.project_name = json_data['project_name']

        assert isinstance(json_data['project_id'], str)
        self.project_id = json_data['project_id']

        assert isinstance(json_data['task_list'], list)
        self.task_list = json_data['task_list']

    @classmethod
    def create_project(cls,
                       project_name: str,
                       task_list: List[TaskType],
                       categories: List[str]) -> 'Project':
        """Create a new project.
        Args:
            project_name: Name of the project.
            task_list: List of tasks to train for.
            categories: The list of categories to train for.

        Returns:
            A Project object.
        """
        payload = {
            'project_name': project_name,
            'task_list': task_list,
            'category_list': categories,
            'username': 'root',
        }

        json_data = cls.client.send_request(
            request_type=RequestType.POST,
            route=RouteType.CREATE_PROJECT,
            payload=payload)

        assert json_data is not None

        project_instance = cls()
        project_instance.populate_from_json(json_data)

        return project_instance

    @classmethod
    def from_id(cls, project_id: str) -> 'Optional[Project]':
        """Get a Project instance from an existing id.

        Args:
            project_id:
        """
        payload = {'project_id': project_id}
        json_data = cls.client.send_request(
            request_type=RequestType.GET,
            route=RouteType.PROJECT_LOOKUP,
            payload=payload)

        if not json_data:
            return None

        project_instance = cls()
        project_instance.populate_from_json(json_data)

        return project_instance

    @classmethod
    def list_projects(cls) -> None:
        """List the project created.
        """
        json_data = cls.client.send_request(
            request_type=RequestType.GET,
            route=RouteType.LIST_PROJECTS,
            payload=None,
        )

        assert json_data is not None

        project_list: List[Dict[str, Any]] = json_data['project_list']

        headers = ['project_id', 'project_name', 'tasks', 'status']
        rows = [[
            proj['project_id'],
            proj['project_name'],
            proj['task_list'],
            proj['status'],
        ] for proj in project_list]
        print(tabulate.tabulate(rows, headers=headers))

    def sample(self,
               sampling_strategy: SamplingStrategy,
               num_sample: int) -> typing.List[Sample]:
        """Sample the data from the existing data.

        Arguments:
            sampling_strategy: Specify the sampling strategy.
        """
        payload = {
            'project_id': self.project_id,
            'sampling_strategy': sampling_strategy,
            'num_sample': num_sample
        }

        json_data = self.client.send_request(
            request_type=RequestType.GET,
            route=RouteType.SAMPLING,
            payload=payload
        )

        assert json_data is not None

        sample_list = [
            Sample(file_name)
            for file_name in json_data['sample_list']
        ]

        return sample_list

    def upload_data(self, datapath: str) -> Optional[List[str]]:
        """Upload the data to the server.

        Arguments:
            dataset_name {str} -- Designated name for this dataset, it
                could be an s3 data path.
            datapath {str} -- Path to the tar file to upload.
        """
        if not os.path.exists(datapath):
            logger.error('%s is not available', datapath)
            return None

        size_in_mb = float(os.path.getsize(datapath)) / 1e6

        if size_in_mb > 100:
            logger.error("File size > 100MB, use upload_s3 instead.")
            return None

        with open(datapath, 'rb') as file_handle:
            files = {
                'file': file_handle,
                'data': json.dumps({
                    'project_id': self.project_id,
                    'username': 'root',
                })
            }

            json_data = self.client.send_request(
                request_type=RequestType.POST,
                route=RouteType.UPLOAD,
                payload=None,
                files=files)

            assert json_data is not None

            uploaded_file_list: List[str] = json_data['uploaded_files']

            logger.info(
                'Successfully uploaded the file, found %d image files.',
                len(uploaded_file_list))

            return uploaded_file_list

    def start_annotation(
            self,
            dataset_name: str,
            sample_list: typing.List[Sample],
            task_list: Union[List[TaskType], None] = None) -> AnnotationTask:
        """Start the annotation process.

        Args:
            dataset_name {str}: Name of the dataset.
            sample_list: A list of sample to be annotated by Scalabel.
            task_list: The list of tasks to annotate, if None, defaulted to the
                list from project creation.
        """
        payload = {
            "sample_list": jsonpickle.encode(sample_list),
            'dataset_name': dataset_name,
            "task_list": task_list,
            "project_id": self.project_id,
            "username": "root",
        }

        json_data = self.client.send_request(
            request_type=RequestType.POST,
            route=RouteType.START_ANNOTATION,
            payload=payload,
        )

        assert json_data is not None
        logger.info('New Scalabel task is initialized.')

        # TODO(phuc): Make a real annotation task. This makes a dummy
        # AnnotationTask for now.
        return AnnotationTask('abc')

    def create_trainer(self,
                       dataset_name: str,
                       train_val_split: float = 0.8,
                       min_annotation_per_class: int = 50) -> Trainer:
        """Start the training process using the annotated files.

        Args:
            dataset_name: Name of dataset.
            train_val_split: Split ratio between training and validation.
            min_annotation_per_class: Minimum number of annotations per class
                to start training.

        Returns:
            A Trainer object.
        """
        payload = {
            'username': 'root',
            'project_id': self.project_id,
            'dataset_name': dataset_name,
            'train_val_split': train_val_split,
            'min_annotation_per_class': min_annotation_per_class,
        }

        json_data = self.client.send_request(
            request_type=RequestType.POST,
            route=RouteType.CREATE_TRAINER,
            payload=payload
        )

        assert json_data is not None

        trainer = Trainer(client=self.client)
        trainer.populate_from_json(json_data)

        return trainer

    def list_trainers(self) -> bool:
        """Print the existing trainers for this project.
        """
        payload = {
            'project_id': self.project_id
        }

        json_data = self.client.send_request(
            request_type=RequestType.GET,
            route=RouteType.LIST_TRAINER,
            payload=payload
        )

        assert json_data is not None

        trainer_list = json_data['trainer_list']

        headers = ['trainer_id', 'model', 'dataset', 'tensorboard', 'status']
        rows = [
            [
                trainer_dict['trainer_id'],
                trainer_dict['model'],
                trainer_dict['dataset'],
                trainer_dict['tensorboard'],
                trainer_dict['status'],
            ]
            for trainer_dict in trainer_list
        ]
        print(tabulate.tabulate(rows, headers=headers))
        return True

    def __repr__(self) -> str:
        return '<Project %s project_id=%s> %s' % (
            self.project_name, self.project_id, str(self.task_list))
