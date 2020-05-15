"""
Main interface for serverlessrepo service client paginators.

Usage::

    import boto3
    from mypy_boto3.serverlessrepo import (
        ListApplicationDependenciesPaginator,
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
    )

    client: ServerlessApplicationRepositoryClient = boto3.client("serverlessrepo")

    list_application_dependencies_paginator: ListApplicationDependenciesPaginator = client.get_paginator("list_application_dependencies")
    list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from typing import Iterator, TYPE_CHECKING
from botocore.paginate import Paginator as Boto3Paginator
from mypy_boto3_serverlessrepo.type_defs import (
    ListApplicationDependenciesResponseTypeDef,
    ListApplicationVersionsResponseTypeDef,
    ListApplicationsResponseTypeDef,
    PaginatorConfigTypeDef,
)


__all__ = (
    "ListApplicationDependenciesPaginator",
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
)


class ListApplicationDependenciesPaginator(Boto3Paginator):
    """
    [Paginator.ListApplicationDependencies documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplicationDependencies)
    """

    def paginate(
        self,
        ApplicationId: str,
        SemanticVersion: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListApplicationDependenciesResponseTypeDef]:
        """
        [ListApplicationDependencies.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplicationDependencies.paginate)
        """


class ListApplicationVersionsPaginator(Boto3Paginator):
    """
    [Paginator.ListApplicationVersions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplicationVersions)
    """

    def paginate(
        self, ApplicationId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListApplicationVersionsResponseTypeDef]:
        """
        [ListApplicationVersions.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplicationVersions.paginate)
        """


class ListApplicationsPaginator(Boto3Paginator):
    """
    [Paginator.ListApplications documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplications)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListApplicationsResponseTypeDef]:
        """
        [ListApplications.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplications.paginate)
        """
