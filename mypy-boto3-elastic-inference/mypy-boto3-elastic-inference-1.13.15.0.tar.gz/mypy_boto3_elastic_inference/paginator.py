"""
Main interface for elastic-inference service client paginators.

Usage::

    import boto3
    from mypy_boto3.elastic_inference import (
        DescribeAcceleratorsPaginator,
    )

    client: ElasticInferenceClient = boto3.client("elastic-inference")

    describe_accelerators_paginator: DescribeAcceleratorsPaginator = client.get_paginator("describe_accelerators")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from typing import Iterator, List, TYPE_CHECKING
from botocore.paginate import Paginator as Boto3Paginator
from mypy_boto3_elastic_inference.type_defs import (
    DescribeAcceleratorsResponseTypeDef,
    FilterTypeDef,
    PaginatorConfigTypeDef,
)


__all__ = ("DescribeAcceleratorsPaginator",)


class DescribeAcceleratorsPaginator(Boto3Paginator):
    """
    [Paginator.DescribeAccelerators documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.15/reference/services/elastic-inference.html#ElasticInference.Paginator.DescribeAccelerators)
    """

    def paginate(
        self,
        acceleratorIds: List[str] = None,
        filters: List[FilterTypeDef] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeAcceleratorsResponseTypeDef]:
        """
        [DescribeAccelerators.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.15/reference/services/elastic-inference.html#ElasticInference.Paginator.DescribeAccelerators.paginate)
        """
