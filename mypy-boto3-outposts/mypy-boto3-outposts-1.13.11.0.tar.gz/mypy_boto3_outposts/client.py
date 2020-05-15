"""
Main interface for outposts service client

Usage::

    import boto3
    from mypy_boto3.outposts import OutpostsClient

    session = boto3.Session()

    client: OutpostsClient = boto3.client("outposts")
    session_client: OutpostsClient = session.client("outposts")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from typing import Any, Dict, TYPE_CHECKING, Type
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_outposts.type_defs import (
    CreateOutpostOutputTypeDef,
    GetOutpostInstanceTypesOutputTypeDef,
    GetOutpostOutputTypeDef,
    ListOutpostsOutputTypeDef,
    ListSitesOutputTypeDef,
)


__all__ = ("OutpostsClient",)


class Exceptions:
    AccessDeniedException: Type[Boto3ClientError]
    ClientError: Type[Boto3ClientError]
    InternalServerException: Type[Boto3ClientError]
    NotFoundException: Type[Boto3ClientError]
    ServiceQuotaExceededException: Type[Boto3ClientError]
    ValidationException: Type[Boto3ClientError]


class OutpostsClient:
    """
    [Outposts.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/outposts.html#Outposts.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/outposts.html#Outposts.Client.can_paginate)
        """

    def create_outpost(
        self,
        SiteId: str,
        Name: str = None,
        Description: str = None,
        AvailabilityZone: str = None,
        AvailabilityZoneId: str = None,
    ) -> CreateOutpostOutputTypeDef:
        """
        [Client.create_outpost documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/outposts.html#Outposts.Client.create_outpost)
        """

    def delete_outpost(self, OutpostId: str) -> Dict[str, Any]:
        """
        [Client.delete_outpost documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/outposts.html#Outposts.Client.delete_outpost)
        """

    def delete_site(self, SiteId: str) -> Dict[str, Any]:
        """
        [Client.delete_site documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/outposts.html#Outposts.Client.delete_site)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/outposts.html#Outposts.Client.generate_presigned_url)
        """

    def get_outpost(self, OutpostId: str) -> GetOutpostOutputTypeDef:
        """
        [Client.get_outpost documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/outposts.html#Outposts.Client.get_outpost)
        """

    def get_outpost_instance_types(
        self, OutpostId: str, NextToken: str = None, MaxResults: int = None
    ) -> GetOutpostInstanceTypesOutputTypeDef:
        """
        [Client.get_outpost_instance_types documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/outposts.html#Outposts.Client.get_outpost_instance_types)
        """

    def list_outposts(
        self, NextToken: str = None, MaxResults: int = None
    ) -> ListOutpostsOutputTypeDef:
        """
        [Client.list_outposts documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/outposts.html#Outposts.Client.list_outposts)
        """

    def list_sites(self, NextToken: str = None, MaxResults: int = None) -> ListSitesOutputTypeDef:
        """
        [Client.list_sites documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/outposts.html#Outposts.Client.list_sites)
        """
