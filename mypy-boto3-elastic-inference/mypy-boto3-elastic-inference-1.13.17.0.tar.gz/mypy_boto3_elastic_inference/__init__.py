"""
Main interface for elastic-inference service.

Usage::

    import boto3
    from mypy_boto3.elastic_inference import (
        Client,
        DescribeAcceleratorsPaginator,
        ElasticInferenceClient,
        )

    session = boto3.Session()

    client: ElasticInferenceClient = boto3.client("elastic-inference")
    session_client: ElasticInferenceClient = session.client("elastic-inference")

    describe_accelerators_paginator: DescribeAcceleratorsPaginator = client.get_paginator("describe_accelerators")
"""
from mypy_boto3_elastic_inference.client import (
    ElasticInferenceClient as Client,
    ElasticInferenceClient,
)
from mypy_boto3_elastic_inference.paginator import DescribeAcceleratorsPaginator


__all__ = ("Client", "DescribeAcceleratorsPaginator", "ElasticInferenceClient")
