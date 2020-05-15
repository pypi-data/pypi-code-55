"""
Main interface for kinesis-video-signaling service client

Usage::

    import boto3
    from mypy_boto3.kinesis_video_signaling import KinesisVideoSignalingChannelsClient

    session = boto3.Session()

    client: KinesisVideoSignalingChannelsClient = boto3.client("kinesis-video-signaling")
    session_client: KinesisVideoSignalingChannelsClient = session.client("kinesis-video-signaling")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, TYPE_CHECKING, Type
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_kinesis_video_signaling.type_defs import (
    GetIceServerConfigResponseTypeDef,
    SendAlexaOfferToMasterResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("KinesisVideoSignalingChannelsClient",)


class Exceptions:
    ClientError: Type[Boto3ClientError]
    ClientLimitExceededException: Type[Boto3ClientError]
    InvalidArgumentException: Type[Boto3ClientError]
    InvalidClientException: Type[Boto3ClientError]
    NotAuthorizedException: Type[Boto3ClientError]
    ResourceNotFoundException: Type[Boto3ClientError]
    SessionExpiredException: Type[Boto3ClientError]


class KinesisVideoSignalingChannelsClient:
    """
    [KinesisVideoSignalingChannels.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/kinesis-video-signaling.html#KinesisVideoSignalingChannels.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/kinesis-video-signaling.html#KinesisVideoSignalingChannels.Client.can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/kinesis-video-signaling.html#KinesisVideoSignalingChannels.Client.generate_presigned_url)
        """

    def get_ice_server_config(
        self,
        ChannelARN: str,
        ClientId: str = None,
        Service: Literal["TURN"] = None,
        Username: str = None,
    ) -> GetIceServerConfigResponseTypeDef:
        """
        [Client.get_ice_server_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/kinesis-video-signaling.html#KinesisVideoSignalingChannels.Client.get_ice_server_config)
        """

    def send_alexa_offer_to_master(
        self, ChannelARN: str, SenderClientId: str, MessagePayload: str
    ) -> SendAlexaOfferToMasterResponseTypeDef:
        """
        [Client.send_alexa_offer_to_master documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/kinesis-video-signaling.html#KinesisVideoSignalingChannels.Client.send_alexa_offer_to_master)
        """
