"""
Main interface for synthetics service type definitions.

Usage::

    from mypy_boto3.synthetics.type_defs import CanaryCodeInputTypeDef

    data: CanaryCodeInputTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CanaryCodeInputTypeDef",
    "CanaryRunConfigInputTypeDef",
    "CanaryScheduleInputTypeDef",
    "CanaryCodeOutputTypeDef",
    "CanaryRunConfigOutputTypeDef",
    "CanaryScheduleOutputTypeDef",
    "CanaryStatusTypeDef",
    "CanaryTimelineTypeDef",
    "VpcConfigOutputTypeDef",
    "CanaryTypeDef",
    "CreateCanaryResponseTypeDef",
    "CanaryRunStatusTypeDef",
    "CanaryRunTimelineTypeDef",
    "CanaryRunTypeDef",
    "CanaryLastRunTypeDef",
    "DescribeCanariesLastRunResponseTypeDef",
    "DescribeCanariesResponseTypeDef",
    "RuntimeVersionTypeDef",
    "DescribeRuntimeVersionsResponseTypeDef",
    "GetCanaryResponseTypeDef",
    "GetCanaryRunsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "VpcConfigInputTypeDef",
)

_RequiredCanaryCodeInputTypeDef = TypedDict("_RequiredCanaryCodeInputTypeDef", {"Handler": str})
_OptionalCanaryCodeInputTypeDef = TypedDict(
    "_OptionalCanaryCodeInputTypeDef",
    {"S3Bucket": str, "S3Key": str, "S3Version": str, "ZipFile": Union[bytes, IO]},
    total=False,
)


class CanaryCodeInputTypeDef(_RequiredCanaryCodeInputTypeDef, _OptionalCanaryCodeInputTypeDef):
    pass


_RequiredCanaryRunConfigInputTypeDef = TypedDict(
    "_RequiredCanaryRunConfigInputTypeDef", {"TimeoutInSeconds": int}
)
_OptionalCanaryRunConfigInputTypeDef = TypedDict(
    "_OptionalCanaryRunConfigInputTypeDef", {"MemoryInMB": int}, total=False
)


class CanaryRunConfigInputTypeDef(
    _RequiredCanaryRunConfigInputTypeDef, _OptionalCanaryRunConfigInputTypeDef
):
    pass


_RequiredCanaryScheduleInputTypeDef = TypedDict(
    "_RequiredCanaryScheduleInputTypeDef", {"Expression": str}
)
_OptionalCanaryScheduleInputTypeDef = TypedDict(
    "_OptionalCanaryScheduleInputTypeDef", {"DurationInSeconds": int}, total=False
)


class CanaryScheduleInputTypeDef(
    _RequiredCanaryScheduleInputTypeDef, _OptionalCanaryScheduleInputTypeDef
):
    pass


CanaryCodeOutputTypeDef = TypedDict(
    "CanaryCodeOutputTypeDef", {"SourceLocationArn": str, "Handler": str}, total=False
)

CanaryRunConfigOutputTypeDef = TypedDict(
    "CanaryRunConfigOutputTypeDef", {"TimeoutInSeconds": int, "MemoryInMB": int}, total=False
)

CanaryScheduleOutputTypeDef = TypedDict(
    "CanaryScheduleOutputTypeDef", {"Expression": str, "DurationInSeconds": int}, total=False
)

CanaryStatusTypeDef = TypedDict(
    "CanaryStatusTypeDef",
    {
        "State": Literal[
            "CREATING",
            "READY",
            "STARTING",
            "RUNNING",
            "UPDATING",
            "STOPPING",
            "STOPPED",
            "ERROR",
            "DELETING",
        ],
        "StateReason": str,
        "StateReasonCode": Literal["INVALID_PERMISSIONS"],
    },
    total=False,
)

CanaryTimelineTypeDef = TypedDict(
    "CanaryTimelineTypeDef",
    {
        "Created": datetime,
        "LastModified": datetime,
        "LastStarted": datetime,
        "LastStopped": datetime,
    },
    total=False,
)

VpcConfigOutputTypeDef = TypedDict(
    "VpcConfigOutputTypeDef",
    {"VpcId": str, "SubnetIds": List[str], "SecurityGroupIds": List[str]},
    total=False,
)

CanaryTypeDef = TypedDict(
    "CanaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Code": CanaryCodeOutputTypeDef,
        "ExecutionRoleArn": str,
        "Schedule": CanaryScheduleOutputTypeDef,
        "RunConfig": CanaryRunConfigOutputTypeDef,
        "SuccessRetentionPeriodInDays": int,
        "FailureRetentionPeriodInDays": int,
        "Status": CanaryStatusTypeDef,
        "Timeline": CanaryTimelineTypeDef,
        "ArtifactS3Location": str,
        "EngineArn": str,
        "RuntimeVersion": str,
        "VpcConfig": VpcConfigOutputTypeDef,
        "Tags": Dict[str, str],
    },
    total=False,
)

CreateCanaryResponseTypeDef = TypedDict(
    "CreateCanaryResponseTypeDef", {"Canary": CanaryTypeDef}, total=False
)

CanaryRunStatusTypeDef = TypedDict(
    "CanaryRunStatusTypeDef",
    {
        "State": Literal["RUNNING", "PASSED", "FAILED"],
        "StateReason": str,
        "StateReasonCode": Literal["CANARY_FAILURE", "EXECUTION_FAILURE"],
    },
    total=False,
)

CanaryRunTimelineTypeDef = TypedDict(
    "CanaryRunTimelineTypeDef", {"Started": datetime, "Completed": datetime}, total=False
)

CanaryRunTypeDef = TypedDict(
    "CanaryRunTypeDef",
    {
        "Name": str,
        "Status": CanaryRunStatusTypeDef,
        "Timeline": CanaryRunTimelineTypeDef,
        "ArtifactS3Location": str,
    },
    total=False,
)

CanaryLastRunTypeDef = TypedDict(
    "CanaryLastRunTypeDef", {"CanaryName": str, "LastRun": CanaryRunTypeDef}, total=False
)

DescribeCanariesLastRunResponseTypeDef = TypedDict(
    "DescribeCanariesLastRunResponseTypeDef",
    {"CanariesLastRun": List[CanaryLastRunTypeDef], "NextToken": str},
    total=False,
)

DescribeCanariesResponseTypeDef = TypedDict(
    "DescribeCanariesResponseTypeDef",
    {"Canaries": List[CanaryTypeDef], "NextToken": str},
    total=False,
)

RuntimeVersionTypeDef = TypedDict(
    "RuntimeVersionTypeDef",
    {"VersionName": str, "Description": str, "ReleaseDate": datetime, "DeprecationDate": datetime},
    total=False,
)

DescribeRuntimeVersionsResponseTypeDef = TypedDict(
    "DescribeRuntimeVersionsResponseTypeDef",
    {"RuntimeVersions": List[RuntimeVersionTypeDef], "NextToken": str},
    total=False,
)

GetCanaryResponseTypeDef = TypedDict(
    "GetCanaryResponseTypeDef", {"Canary": CanaryTypeDef}, total=False
)

GetCanaryRunsResponseTypeDef = TypedDict(
    "GetCanaryRunsResponseTypeDef",
    {"CanaryRuns": List[CanaryRunTypeDef], "NextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

VpcConfigInputTypeDef = TypedDict(
    "VpcConfigInputTypeDef", {"SubnetIds": List[str], "SecurityGroupIds": List[str]}, total=False
)
