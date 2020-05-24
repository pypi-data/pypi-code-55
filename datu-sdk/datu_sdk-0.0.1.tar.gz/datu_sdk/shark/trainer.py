"""Class definition for the client-side Trainer object.
"""
from typing import Dict, Union
from .base_api import BaseAPI
from .common.logging import logger
from .common.enums import RequestType, RouteType


JSONTYPE = Dict[str, Union[str, str]]


class Trainer(BaseAPI):
    """Class definition for the trainer.
    """

    trainer_id: str
    project_id: str

    def populate_from_json(self, json_data: JSONTYPE) -> None:
        """Populate from json.
        """
        required_fields = set(['project_id', 'trainer_id'])
        missing_keys = required_fields - set(json_data.keys())

        if missing_keys:
            logger.error('Required fields are missing: %s', str(missing_keys))
            return

        assert isinstance(json_data['project_id'], str)
        self.project_id = json_data['project_id']

        assert isinstance(json_data['trainer_id'], str)
        self.trainer_id = json_data['trainer_id']

    def start_training(self) -> None:
        """Kickstart the training for this trainer.

        Args:
            force {bool} -- Whether to force the training even when the trainer
                is not ready.
        """
        payload = {
            'username': 'root',
            'trainer_id': self.trainer_id,
            'project_id': self.project_id,
        }
        json_data = self.client.send_request(
            request_type=RequestType.POST,
            route=RouteType.START_TRAINING,
            payload=payload
        )

        assert json_data is not None

        if json_data['status'] == 'success':
            logger.error('Error: %s', json_data['message'])
