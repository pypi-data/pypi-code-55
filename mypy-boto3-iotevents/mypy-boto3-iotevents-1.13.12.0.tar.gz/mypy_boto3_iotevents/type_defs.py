"""
Main interface for iotevents service type definitions.

Usage::

    from mypy_boto3.iotevents.type_defs import DetectorModelConfigurationTypeDef

    data: DetectorModelConfigurationTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DetectorModelConfigurationTypeDef",
    "CreateDetectorModelResponseTypeDef",
    "InputConfigurationTypeDef",
    "CreateInputResponseTypeDef",
    "ClearTimerActionTypeDef",
    "PayloadTypeDef",
    "DynamoDBActionTypeDef",
    "DynamoDBv2ActionTypeDef",
    "FirehoseActionTypeDef",
    "IotEventsActionTypeDef",
    "AssetPropertyTimestampTypeDef",
    "AssetPropertyVariantTypeDef",
    "AssetPropertyValueTypeDef",
    "IotSiteWiseActionTypeDef",
    "IotTopicPublishActionTypeDef",
    "LambdaActionTypeDef",
    "ResetTimerActionTypeDef",
    "SNSTopicPublishActionTypeDef",
    "SetTimerActionTypeDef",
    "SetVariableActionTypeDef",
    "SqsActionTypeDef",
    "ActionTypeDef",
    "EventTypeDef",
    "OnEnterLifecycleTypeDef",
    "OnExitLifecycleTypeDef",
    "TransitionEventTypeDef",
    "OnInputLifecycleTypeDef",
    "StateTypeDef",
    "DetectorModelDefinitionTypeDef",
    "DetectorModelTypeDef",
    "DescribeDetectorModelResponseTypeDef",
    "AttributeTypeDef",
    "InputDefinitionTypeDef",
    "InputTypeDef",
    "DescribeInputResponseTypeDef",
    "DetectorDebugOptionTypeDef",
    "LoggingOptionsTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "DetectorModelVersionSummaryTypeDef",
    "ListDetectorModelVersionsResponseTypeDef",
    "DetectorModelSummaryTypeDef",
    "ListDetectorModelsResponseTypeDef",
    "InputSummaryTypeDef",
    "ListInputsResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateDetectorModelResponseTypeDef",
    "UpdateInputResponseTypeDef",
)

DetectorModelConfigurationTypeDef = TypedDict(
    "DetectorModelConfigurationTypeDef",
    {
        "detectorModelName": str,
        "detectorModelVersion": str,
        "detectorModelDescription": str,
        "detectorModelArn": str,
        "roleArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": Literal[
            "ACTIVE", "ACTIVATING", "INACTIVE", "DEPRECATED", "DRAFT", "PAUSED", "FAILED"
        ],
        "key": str,
        "evaluationMethod": Literal["BATCH", "SERIAL"],
    },
    total=False,
)

CreateDetectorModelResponseTypeDef = TypedDict(
    "CreateDetectorModelResponseTypeDef",
    {"detectorModelConfiguration": DetectorModelConfigurationTypeDef},
    total=False,
)

_RequiredInputConfigurationTypeDef = TypedDict(
    "_RequiredInputConfigurationTypeDef",
    {
        "inputName": str,
        "inputArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": Literal["CREATING", "UPDATING", "ACTIVE", "DELETING"],
    },
)
_OptionalInputConfigurationTypeDef = TypedDict(
    "_OptionalInputConfigurationTypeDef", {"inputDescription": str}, total=False
)


class InputConfigurationTypeDef(
    _RequiredInputConfigurationTypeDef, _OptionalInputConfigurationTypeDef
):
    pass


CreateInputResponseTypeDef = TypedDict(
    "CreateInputResponseTypeDef", {"inputConfiguration": InputConfigurationTypeDef}, total=False
)

ClearTimerActionTypeDef = TypedDict("ClearTimerActionTypeDef", {"timerName": str})

PayloadTypeDef = TypedDict(
    "PayloadTypeDef", {"contentExpression": str, "type": Literal["STRING", "JSON"]}
)

_RequiredDynamoDBActionTypeDef = TypedDict(
    "_RequiredDynamoDBActionTypeDef", {"hashKeyField": str, "hashKeyValue": str, "tableName": str}
)
_OptionalDynamoDBActionTypeDef = TypedDict(
    "_OptionalDynamoDBActionTypeDef",
    {
        "hashKeyType": str,
        "rangeKeyType": str,
        "rangeKeyField": str,
        "rangeKeyValue": str,
        "operation": str,
        "payloadField": str,
        "payload": PayloadTypeDef,
    },
    total=False,
)


class DynamoDBActionTypeDef(_RequiredDynamoDBActionTypeDef, _OptionalDynamoDBActionTypeDef):
    pass


_RequiredDynamoDBv2ActionTypeDef = TypedDict("_RequiredDynamoDBv2ActionTypeDef", {"tableName": str})
_OptionalDynamoDBv2ActionTypeDef = TypedDict(
    "_OptionalDynamoDBv2ActionTypeDef", {"payload": PayloadTypeDef}, total=False
)


class DynamoDBv2ActionTypeDef(_RequiredDynamoDBv2ActionTypeDef, _OptionalDynamoDBv2ActionTypeDef):
    pass


_RequiredFirehoseActionTypeDef = TypedDict(
    "_RequiredFirehoseActionTypeDef", {"deliveryStreamName": str}
)
_OptionalFirehoseActionTypeDef = TypedDict(
    "_OptionalFirehoseActionTypeDef", {"separator": str, "payload": PayloadTypeDef}, total=False
)


class FirehoseActionTypeDef(_RequiredFirehoseActionTypeDef, _OptionalFirehoseActionTypeDef):
    pass


_RequiredIotEventsActionTypeDef = TypedDict("_RequiredIotEventsActionTypeDef", {"inputName": str})
_OptionalIotEventsActionTypeDef = TypedDict(
    "_OptionalIotEventsActionTypeDef", {"payload": PayloadTypeDef}, total=False
)


class IotEventsActionTypeDef(_RequiredIotEventsActionTypeDef, _OptionalIotEventsActionTypeDef):
    pass


_RequiredAssetPropertyTimestampTypeDef = TypedDict(
    "_RequiredAssetPropertyTimestampTypeDef", {"timeInSeconds": str}
)
_OptionalAssetPropertyTimestampTypeDef = TypedDict(
    "_OptionalAssetPropertyTimestampTypeDef", {"offsetInNanos": str}, total=False
)


class AssetPropertyTimestampTypeDef(
    _RequiredAssetPropertyTimestampTypeDef, _OptionalAssetPropertyTimestampTypeDef
):
    pass


AssetPropertyVariantTypeDef = TypedDict(
    "AssetPropertyVariantTypeDef",
    {"stringValue": str, "integerValue": str, "doubleValue": str, "booleanValue": str},
    total=False,
)

_RequiredAssetPropertyValueTypeDef = TypedDict(
    "_RequiredAssetPropertyValueTypeDef", {"value": AssetPropertyVariantTypeDef}
)
_OptionalAssetPropertyValueTypeDef = TypedDict(
    "_OptionalAssetPropertyValueTypeDef",
    {"timestamp": AssetPropertyTimestampTypeDef, "quality": str},
    total=False,
)


class AssetPropertyValueTypeDef(
    _RequiredAssetPropertyValueTypeDef, _OptionalAssetPropertyValueTypeDef
):
    pass


_RequiredIotSiteWiseActionTypeDef = TypedDict(
    "_RequiredIotSiteWiseActionTypeDef", {"propertyValue": AssetPropertyValueTypeDef}
)
_OptionalIotSiteWiseActionTypeDef = TypedDict(
    "_OptionalIotSiteWiseActionTypeDef",
    {"entryId": str, "assetId": str, "propertyId": str, "propertyAlias": str},
    total=False,
)


class IotSiteWiseActionTypeDef(
    _RequiredIotSiteWiseActionTypeDef, _OptionalIotSiteWiseActionTypeDef
):
    pass


_RequiredIotTopicPublishActionTypeDef = TypedDict(
    "_RequiredIotTopicPublishActionTypeDef", {"mqttTopic": str}
)
_OptionalIotTopicPublishActionTypeDef = TypedDict(
    "_OptionalIotTopicPublishActionTypeDef", {"payload": PayloadTypeDef}, total=False
)


class IotTopicPublishActionTypeDef(
    _RequiredIotTopicPublishActionTypeDef, _OptionalIotTopicPublishActionTypeDef
):
    pass


_RequiredLambdaActionTypeDef = TypedDict("_RequiredLambdaActionTypeDef", {"functionArn": str})
_OptionalLambdaActionTypeDef = TypedDict(
    "_OptionalLambdaActionTypeDef", {"payload": PayloadTypeDef}, total=False
)


class LambdaActionTypeDef(_RequiredLambdaActionTypeDef, _OptionalLambdaActionTypeDef):
    pass


ResetTimerActionTypeDef = TypedDict("ResetTimerActionTypeDef", {"timerName": str})

_RequiredSNSTopicPublishActionTypeDef = TypedDict(
    "_RequiredSNSTopicPublishActionTypeDef", {"targetArn": str}
)
_OptionalSNSTopicPublishActionTypeDef = TypedDict(
    "_OptionalSNSTopicPublishActionTypeDef", {"payload": PayloadTypeDef}, total=False
)


class SNSTopicPublishActionTypeDef(
    _RequiredSNSTopicPublishActionTypeDef, _OptionalSNSTopicPublishActionTypeDef
):
    pass


_RequiredSetTimerActionTypeDef = TypedDict("_RequiredSetTimerActionTypeDef", {"timerName": str})
_OptionalSetTimerActionTypeDef = TypedDict(
    "_OptionalSetTimerActionTypeDef", {"seconds": int, "durationExpression": str}, total=False
)


class SetTimerActionTypeDef(_RequiredSetTimerActionTypeDef, _OptionalSetTimerActionTypeDef):
    pass


SetVariableActionTypeDef = TypedDict(
    "SetVariableActionTypeDef", {"variableName": str, "value": str}
)

_RequiredSqsActionTypeDef = TypedDict("_RequiredSqsActionTypeDef", {"queueUrl": str})
_OptionalSqsActionTypeDef = TypedDict(
    "_OptionalSqsActionTypeDef", {"useBase64": bool, "payload": PayloadTypeDef}, total=False
)


class SqsActionTypeDef(_RequiredSqsActionTypeDef, _OptionalSqsActionTypeDef):
    pass


ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "setVariable": SetVariableActionTypeDef,
        "sns": SNSTopicPublishActionTypeDef,
        "iotTopicPublish": IotTopicPublishActionTypeDef,
        "setTimer": SetTimerActionTypeDef,
        "clearTimer": ClearTimerActionTypeDef,
        "resetTimer": ResetTimerActionTypeDef,
        "lambda": LambdaActionTypeDef,
        "iotEvents": IotEventsActionTypeDef,
        "sqs": SqsActionTypeDef,
        "firehose": FirehoseActionTypeDef,
        "dynamoDB": DynamoDBActionTypeDef,
        "dynamoDBv2": DynamoDBv2ActionTypeDef,
        "iotSiteWise": IotSiteWiseActionTypeDef,
    },
    total=False,
)

_RequiredEventTypeDef = TypedDict("_RequiredEventTypeDef", {"eventName": str})
_OptionalEventTypeDef = TypedDict(
    "_OptionalEventTypeDef", {"condition": str, "actions": List[ActionTypeDef]}, total=False
)


class EventTypeDef(_RequiredEventTypeDef, _OptionalEventTypeDef):
    pass


OnEnterLifecycleTypeDef = TypedDict(
    "OnEnterLifecycleTypeDef", {"events": List[EventTypeDef]}, total=False
)

OnExitLifecycleTypeDef = TypedDict(
    "OnExitLifecycleTypeDef", {"events": List[EventTypeDef]}, total=False
)

_RequiredTransitionEventTypeDef = TypedDict(
    "_RequiredTransitionEventTypeDef", {"eventName": str, "condition": str, "nextState": str}
)
_OptionalTransitionEventTypeDef = TypedDict(
    "_OptionalTransitionEventTypeDef", {"actions": List[ActionTypeDef]}, total=False
)


class TransitionEventTypeDef(_RequiredTransitionEventTypeDef, _OptionalTransitionEventTypeDef):
    pass


OnInputLifecycleTypeDef = TypedDict(
    "OnInputLifecycleTypeDef",
    {"events": List[EventTypeDef], "transitionEvents": List[TransitionEventTypeDef]},
    total=False,
)

_RequiredStateTypeDef = TypedDict("_RequiredStateTypeDef", {"stateName": str})
_OptionalStateTypeDef = TypedDict(
    "_OptionalStateTypeDef",
    {
        "onInput": OnInputLifecycleTypeDef,
        "onEnter": OnEnterLifecycleTypeDef,
        "onExit": OnExitLifecycleTypeDef,
    },
    total=False,
)


class StateTypeDef(_RequiredStateTypeDef, _OptionalStateTypeDef):
    pass


DetectorModelDefinitionTypeDef = TypedDict(
    "DetectorModelDefinitionTypeDef", {"states": List[StateTypeDef], "initialStateName": str}
)

DetectorModelTypeDef = TypedDict(
    "DetectorModelTypeDef",
    {
        "detectorModelDefinition": DetectorModelDefinitionTypeDef,
        "detectorModelConfiguration": DetectorModelConfigurationTypeDef,
    },
    total=False,
)

DescribeDetectorModelResponseTypeDef = TypedDict(
    "DescribeDetectorModelResponseTypeDef", {"detectorModel": DetectorModelTypeDef}, total=False
)

AttributeTypeDef = TypedDict("AttributeTypeDef", {"jsonPath": str})

InputDefinitionTypeDef = TypedDict("InputDefinitionTypeDef", {"attributes": List[AttributeTypeDef]})

InputTypeDef = TypedDict(
    "InputTypeDef",
    {"inputConfiguration": InputConfigurationTypeDef, "inputDefinition": InputDefinitionTypeDef},
    total=False,
)

DescribeInputResponseTypeDef = TypedDict(
    "DescribeInputResponseTypeDef", {"input": InputTypeDef}, total=False
)

_RequiredDetectorDebugOptionTypeDef = TypedDict(
    "_RequiredDetectorDebugOptionTypeDef", {"detectorModelName": str}
)
_OptionalDetectorDebugOptionTypeDef = TypedDict(
    "_OptionalDetectorDebugOptionTypeDef", {"keyValue": str}, total=False
)


class DetectorDebugOptionTypeDef(
    _RequiredDetectorDebugOptionTypeDef, _OptionalDetectorDebugOptionTypeDef
):
    pass


_RequiredLoggingOptionsTypeDef = TypedDict(
    "_RequiredLoggingOptionsTypeDef",
    {"roleArn": str, "level": Literal["ERROR", "INFO", "DEBUG"], "enabled": bool},
)
_OptionalLoggingOptionsTypeDef = TypedDict(
    "_OptionalLoggingOptionsTypeDef",
    {"detectorDebugOptions": List[DetectorDebugOptionTypeDef]},
    total=False,
)


class LoggingOptionsTypeDef(_RequiredLoggingOptionsTypeDef, _OptionalLoggingOptionsTypeDef):
    pass


DescribeLoggingOptionsResponseTypeDef = TypedDict(
    "DescribeLoggingOptionsResponseTypeDef", {"loggingOptions": LoggingOptionsTypeDef}, total=False
)

DetectorModelVersionSummaryTypeDef = TypedDict(
    "DetectorModelVersionSummaryTypeDef",
    {
        "detectorModelName": str,
        "detectorModelVersion": str,
        "detectorModelArn": str,
        "roleArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": Literal[
            "ACTIVE", "ACTIVATING", "INACTIVE", "DEPRECATED", "DRAFT", "PAUSED", "FAILED"
        ],
        "evaluationMethod": Literal["BATCH", "SERIAL"],
    },
    total=False,
)

ListDetectorModelVersionsResponseTypeDef = TypedDict(
    "ListDetectorModelVersionsResponseTypeDef",
    {"detectorModelVersionSummaries": List[DetectorModelVersionSummaryTypeDef], "nextToken": str},
    total=False,
)

DetectorModelSummaryTypeDef = TypedDict(
    "DetectorModelSummaryTypeDef",
    {"detectorModelName": str, "detectorModelDescription": str, "creationTime": datetime},
    total=False,
)

ListDetectorModelsResponseTypeDef = TypedDict(
    "ListDetectorModelsResponseTypeDef",
    {"detectorModelSummaries": List[DetectorModelSummaryTypeDef], "nextToken": str},
    total=False,
)

InputSummaryTypeDef = TypedDict(
    "InputSummaryTypeDef",
    {
        "inputName": str,
        "inputDescription": str,
        "inputArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": Literal["CREATING", "UPDATING", "ACTIVE", "DELETING"],
    },
    total=False,
)

ListInputsResponseTypeDef = TypedDict(
    "ListInputsResponseTypeDef",
    {"inputSummaries": List[InputSummaryTypeDef], "nextToken": str},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"key": str, "value": str})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": List[TagTypeDef]}, total=False
)

UpdateDetectorModelResponseTypeDef = TypedDict(
    "UpdateDetectorModelResponseTypeDef",
    {"detectorModelConfiguration": DetectorModelConfigurationTypeDef},
    total=False,
)

UpdateInputResponseTypeDef = TypedDict(
    "UpdateInputResponseTypeDef", {"inputConfiguration": InputConfigurationTypeDef}, total=False
)
