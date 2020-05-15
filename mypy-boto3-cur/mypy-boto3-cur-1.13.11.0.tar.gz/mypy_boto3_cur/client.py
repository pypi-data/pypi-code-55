"""
Main interface for cur service client

Usage::

    import boto3
    from mypy_boto3.cur import CostandUsageReportServiceClient

    session = boto3.Session()

    client: CostandUsageReportServiceClient = boto3.client("cur")
    session_client: CostandUsageReportServiceClient = session.client("cur")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, TYPE_CHECKING, Type, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_cur.paginator import DescribeReportDefinitionsPaginator
from mypy_boto3_cur.type_defs import (
    DeleteReportDefinitionResponseTypeDef,
    DescribeReportDefinitionsResponseTypeDef,
    ReportDefinitionTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CostandUsageReportServiceClient",)


class Exceptions:
    ClientError: Type[Boto3ClientError]
    DuplicateReportNameException: Type[Boto3ClientError]
    InternalErrorException: Type[Boto3ClientError]
    ReportLimitReachedException: Type[Boto3ClientError]
    ValidationException: Type[Boto3ClientError]


class CostandUsageReportServiceClient:
    """
    [CostandUsageReportService.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/cur.html#CostandUsageReportService.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/cur.html#CostandUsageReportService.Client.can_paginate)
        """

    def delete_report_definition(
        self, ReportName: str = None
    ) -> DeleteReportDefinitionResponseTypeDef:
        """
        [Client.delete_report_definition documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/cur.html#CostandUsageReportService.Client.delete_report_definition)
        """

    def describe_report_definitions(
        self, MaxResults: int = None, NextToken: str = None
    ) -> DescribeReportDefinitionsResponseTypeDef:
        """
        [Client.describe_report_definitions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/cur.html#CostandUsageReportService.Client.describe_report_definitions)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/cur.html#CostandUsageReportService.Client.generate_presigned_url)
        """

    def modify_report_definition(
        self, ReportName: str, ReportDefinition: ReportDefinitionTypeDef
    ) -> Dict[str, Any]:
        """
        [Client.modify_report_definition documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/cur.html#CostandUsageReportService.Client.modify_report_definition)
        """

    def put_report_definition(self, ReportDefinition: ReportDefinitionTypeDef) -> Dict[str, Any]:
        """
        [Client.put_report_definition documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/cur.html#CostandUsageReportService.Client.put_report_definition)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_report_definitions"]
    ) -> DescribeReportDefinitionsPaginator:
        """
        [Paginator.DescribeReportDefinitions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.11/reference/services/cur.html#CostandUsageReportService.Paginator.DescribeReportDefinitions)
        """
