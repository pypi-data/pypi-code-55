"""
Main interface for resource-groups service client

Usage::

    import boto3
    from mypy_boto3.resource_groups import ResourceGroupsClient

    session = boto3.Session()

    client: ResourceGroupsClient = boto3.client("resource-groups")
    session_client: ResourceGroupsClient = session.client("resource-groups")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, List, TYPE_CHECKING, Type, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_resource_groups.paginator import (
    ListGroupResourcesPaginator,
    ListGroupsPaginator,
    SearchResourcesPaginator,
)
from mypy_boto3_resource_groups.type_defs import (
    CreateGroupOutputTypeDef,
    DeleteGroupOutputTypeDef,
    GetGroupOutputTypeDef,
    GetGroupQueryOutputTypeDef,
    GetTagsOutputTypeDef,
    GroupFilterTypeDef,
    ListGroupResourcesOutputTypeDef,
    ListGroupsOutputTypeDef,
    ResourceFilterTypeDef,
    ResourceQueryTypeDef,
    SearchResourcesOutputTypeDef,
    TagOutputTypeDef,
    UntagOutputTypeDef,
    UpdateGroupOutputTypeDef,
    UpdateGroupQueryOutputTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ResourceGroupsClient",)


class Exceptions:
    BadRequestException: Type[Boto3ClientError]
    ClientError: Type[Boto3ClientError]
    ForbiddenException: Type[Boto3ClientError]
    InternalServerErrorException: Type[Boto3ClientError]
    MethodNotAllowedException: Type[Boto3ClientError]
    NotFoundException: Type[Boto3ClientError]
    TooManyRequestsException: Type[Boto3ClientError]
    UnauthorizedException: Type[Boto3ClientError]


class ResourceGroupsClient:
    """
    [ResourceGroups.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.can_paginate)
        """

    def create_group(
        self,
        Name: str,
        ResourceQuery: ResourceQueryTypeDef,
        Description: str = None,
        Tags: Dict[str, str] = None,
    ) -> CreateGroupOutputTypeDef:
        """
        [Client.create_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.create_group)
        """

    def delete_group(self, GroupName: str) -> DeleteGroupOutputTypeDef:
        """
        [Client.delete_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.delete_group)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.generate_presigned_url)
        """

    def get_group(self, GroupName: str) -> GetGroupOutputTypeDef:
        """
        [Client.get_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.get_group)
        """

    def get_group_query(self, GroupName: str) -> GetGroupQueryOutputTypeDef:
        """
        [Client.get_group_query documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.get_group_query)
        """

    def get_tags(self, Arn: str) -> GetTagsOutputTypeDef:
        """
        [Client.get_tags documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.get_tags)
        """

    def list_group_resources(
        self,
        GroupName: str,
        Filters: List[ResourceFilterTypeDef] = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ListGroupResourcesOutputTypeDef:
        """
        [Client.list_group_resources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.list_group_resources)
        """

    def list_groups(
        self,
        Filters: List[GroupFilterTypeDef] = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ListGroupsOutputTypeDef:
        """
        [Client.list_groups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.list_groups)
        """

    def search_resources(
        self, ResourceQuery: ResourceQueryTypeDef, MaxResults: int = None, NextToken: str = None
    ) -> SearchResourcesOutputTypeDef:
        """
        [Client.search_resources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.search_resources)
        """

    def tag(self, Arn: str, Tags: Dict[str, str]) -> TagOutputTypeDef:
        """
        [Client.tag documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.tag)
        """

    def untag(self, Arn: str, Keys: List[str]) -> UntagOutputTypeDef:
        """
        [Client.untag documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.untag)
        """

    def update_group(self, GroupName: str, Description: str = None) -> UpdateGroupOutputTypeDef:
        """
        [Client.update_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.update_group)
        """

    def update_group_query(
        self, GroupName: str, ResourceQuery: ResourceQueryTypeDef
    ) -> UpdateGroupQueryOutputTypeDef:
        """
        [Client.update_group_query documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Client.update_group_query)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_resources"]
    ) -> ListGroupResourcesPaginator:
        """
        [Paginator.ListGroupResources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroupResources)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Paginator.ListGroups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroups)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_resources"]
    ) -> SearchResourcesPaginator:
        """
        [Paginator.SearchResources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/resource-groups.html#ResourceGroups.Paginator.SearchResources)
        """
