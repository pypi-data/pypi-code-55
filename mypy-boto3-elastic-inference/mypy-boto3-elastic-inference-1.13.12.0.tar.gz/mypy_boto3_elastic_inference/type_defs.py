"""
Main interface for elastic-inference service type definitions.

Usage::

    from mypy_boto3.elastic_inference.type_defs import AcceleratorTypeOfferingTypeDef

    data: AcceleratorTypeOfferingTypeDef = {...}
"""
import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AcceleratorTypeOfferingTypeDef",
    "DescribeAcceleratorOfferingsResponseTypeDef",
    "KeyValuePairTypeDef",
    "MemoryInfoTypeDef",
    "AcceleratorTypeTypeDef",
    "DescribeAcceleratorTypesResponseTypeDef",
    "ElasticInferenceAcceleratorHealthTypeDef",
    "ElasticInferenceAcceleratorTypeDef",
    "DescribeAcceleratorsResponseTypeDef",
    "FilterTypeDef",
    "ListTagsForResourceResultTypeDef",
    "PaginatorConfigTypeDef",
)

AcceleratorTypeOfferingTypeDef = TypedDict(
    "AcceleratorTypeOfferingTypeDef",
    {
        "acceleratorType": str,
        "locationType": Literal["region", "availability-zone", "availability-zone-id"],
        "location": str,
    },
    total=False,
)

DescribeAcceleratorOfferingsResponseTypeDef = TypedDict(
    "DescribeAcceleratorOfferingsResponseTypeDef",
    {"acceleratorTypeOfferings": List[AcceleratorTypeOfferingTypeDef]},
    total=False,
)

KeyValuePairTypeDef = TypedDict("KeyValuePairTypeDef", {"key": str, "value": int}, total=False)

MemoryInfoTypeDef = TypedDict("MemoryInfoTypeDef", {"sizeInMiB": int}, total=False)

AcceleratorTypeTypeDef = TypedDict(
    "AcceleratorTypeTypeDef",
    {
        "acceleratorTypeName": str,
        "memoryInfo": MemoryInfoTypeDef,
        "throughputInfo": List[KeyValuePairTypeDef],
    },
    total=False,
)

DescribeAcceleratorTypesResponseTypeDef = TypedDict(
    "DescribeAcceleratorTypesResponseTypeDef",
    {"acceleratorTypes": List[AcceleratorTypeTypeDef]},
    total=False,
)

ElasticInferenceAcceleratorHealthTypeDef = TypedDict(
    "ElasticInferenceAcceleratorHealthTypeDef", {"status": str}, total=False
)

ElasticInferenceAcceleratorTypeDef = TypedDict(
    "ElasticInferenceAcceleratorTypeDef",
    {
        "acceleratorHealth": ElasticInferenceAcceleratorHealthTypeDef,
        "acceleratorType": str,
        "acceleratorId": str,
        "availabilityZone": str,
        "attachedResource": str,
    },
    total=False,
)

DescribeAcceleratorsResponseTypeDef = TypedDict(
    "DescribeAcceleratorsResponseTypeDef",
    {"acceleratorSet": List[ElasticInferenceAcceleratorTypeDef], "nextToken": str},
    total=False,
)

FilterTypeDef = TypedDict("FilterTypeDef", {"name": str, "values": List[str]}, total=False)

ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef", {"tags": Dict[str, str]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
