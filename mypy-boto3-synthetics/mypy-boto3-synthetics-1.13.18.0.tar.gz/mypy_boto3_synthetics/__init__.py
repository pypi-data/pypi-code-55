"""
Main interface for synthetics service.

Usage::

    import boto3
    from mypy_boto3.synthetics import (
        Client,
        SyntheticsClient,
        )

    session = boto3.Session()

    client: SyntheticsClient = boto3.client("synthetics")
    session_client: SyntheticsClient = session.client("synthetics")
"""
from mypy_boto3_synthetics.client import SyntheticsClient, SyntheticsClient as Client


__all__ = ("Client", "SyntheticsClient")
