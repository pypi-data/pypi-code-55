import json
import base64
from datetime import datetime
from typing import Dict, Optional

from google.cloud.pubsub_v1 import PublisherClient as GooglePubSubClient
from arcane.firebase import generate_token
from google.oauth2 import service_account


class Client(GooglePubSubClient):
    def __init__(self, adscale_key=None):
        credentials = service_account.Credentials.from_service_account_file(adscale_key)
        super().__init__(credentials=credentials)

    def push_to_topic(self, project: str,
                      topic_name: str,
                      parameters: dict,
                      firebase_api_key: str = None,
                      await_response: bool = False):
        """ Add the message to the given topic and if needed, generates  a token to be sent along the message
        to allow authorization"""
        if firebase_api_key:
            token = generate_token(firebase_api_key)
            message = json.dumps({'parameters': parameters, 'token': token}).encode('utf-8')
        else:
            message = json.dumps({'parameters': parameters}).encode('utf-8')

        topic_path = self.topic_path(project, topic_name)
        future = self.publish(topic_path, message)
        if await_response:
            future.result()
        return future
    
    def pubsub_publish_pf_monitoring(self,
                                    topic: str,
                                    project_id:str,
                                    firebase_api_key:str,
                                    monitoring_id: str,
                                    step: str,
                                    entity_id: str,
                                    status: str,
                                    error_message: Optional[str] = None):
        """ publish a message for product flow monitoring"""

        parameters = dict(
            entity_id=entity_id,
            monitoring_id=monitoring_id,
            step=step,
            status=status
        )
        if error_message is not None:
            parameters['error_message'] = error_message

        self.push_to_topic(project=project_id,
                    topic_name=topic,
                    parameters=parameters,
                    firebase_api_key=firebase_api_key,
                    await_response=True)
        print(f"Published {status} message for entity {entity_id} and monitoring_id {monitoring_id}")


def myconverter(o):
    if isinstance(o, datetime):
        return o.strftime('%Y-%m-%dT%H:%M:%SZ')


def pubsub_message_encoder(parameters: dict) -> str:
    """ Encodes a dictionary to a Base64 string """
    return base64.b64encode(json.dumps(parameters, default=myconverter).encode('utf-8')).decode('utf-8')


def pubsub_message_decoder(message_data: str) -> dict:
    """ Decodes a Base64 string to a dictionary """
    return json.loads(base64.b64decode(message_data).decode('utf-8'))


def build_message(message_data: Dict) -> Dict:
    return {'data': pubsub_message_encoder({'parameters': message_data})}
