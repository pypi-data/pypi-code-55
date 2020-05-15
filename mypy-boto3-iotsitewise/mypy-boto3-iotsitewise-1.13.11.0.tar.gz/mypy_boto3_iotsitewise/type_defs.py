"""
Main interface for iotsitewise service type definitions.

Usage::

    from mypy_boto3.iotsitewise.type_defs import AssetModelHierarchyDefinitionTypeDef

    data: AssetModelHierarchyDefinitionTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Any, Dict, IO, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssetModelHierarchyDefinitionTypeDef",
    "AssetModelHierarchyTypeDef",
    "AttributeTypeDef",
    "VariableValueTypeDef",
    "ExpressionVariableTypeDef",
    "TumblingWindowTypeDef",
    "MetricWindowTypeDef",
    "MetricTypeDef",
    "TransformTypeDef",
    "PropertyTypeTypeDef",
    "AssetModelPropertyDefinitionTypeDef",
    "AssetModelPropertyTypeDef",
    "AssetErrorDetailsTypeDef",
    "BatchAssociateProjectAssetsResponseTypeDef",
    "BatchDisassociateProjectAssetsResponseTypeDef",
    "TimeInNanosTypeDef",
    "BatchPutAssetPropertyErrorTypeDef",
    "BatchPutAssetPropertyErrorEntryTypeDef",
    "BatchPutAssetPropertyValueResponseTypeDef",
    "CreateAccessPolicyResponseTypeDef",
    "ErrorDetailsTypeDef",
    "AssetModelStatusTypeDef",
    "CreateAssetModelResponseTypeDef",
    "AssetStatusTypeDef",
    "CreateAssetResponseTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateGatewayResponseTypeDef",
    "MonitorErrorDetailsTypeDef",
    "PortalStatusTypeDef",
    "CreatePortalResponseTypeDef",
    "CreateProjectResponseTypeDef",
    "DeleteAssetModelResponseTypeDef",
    "DeleteAssetResponseTypeDef",
    "DeletePortalResponseTypeDef",
    "GroupIdentityTypeDef",
    "UserIdentityTypeDef",
    "IdentityTypeDef",
    "PortalResourceTypeDef",
    "ProjectResourceTypeDef",
    "ResourceTypeDef",
    "DescribeAccessPolicyResponseTypeDef",
    "DescribeAssetModelResponseTypeDef",
    "PropertyNotificationTypeDef",
    "PropertyTypeDef",
    "DescribeAssetPropertyResponseTypeDef",
    "AssetHierarchyTypeDef",
    "AssetPropertyTypeDef",
    "DescribeAssetResponseTypeDef",
    "DescribeDashboardResponseTypeDef",
    "DescribeGatewayCapabilityConfigurationResponseTypeDef",
    "GatewayCapabilitySummaryTypeDef",
    "GreengrassTypeDef",
    "GatewayPlatformTypeDef",
    "DescribeGatewayResponseTypeDef",
    "LoggingOptionsTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "ImageTypeDef",
    "DescribePortalResponseTypeDef",
    "DescribeProjectResponseTypeDef",
    "AggregatesTypeDef",
    "AggregatedValueTypeDef",
    "GetAssetPropertyAggregatesResponseTypeDef",
    "VariantTypeDef",
    "AssetPropertyValueTypeDef",
    "GetAssetPropertyValueHistoryResponseTypeDef",
    "GetAssetPropertyValueResponseTypeDef",
    "ImageFileTypeDef",
    "AccessPolicySummaryTypeDef",
    "ListAccessPoliciesResponseTypeDef",
    "AssetModelSummaryTypeDef",
    "ListAssetModelsResponseTypeDef",
    "AssetSummaryTypeDef",
    "ListAssetsResponseTypeDef",
    "AssociatedAssetsSummaryTypeDef",
    "ListAssociatedAssetsResponseTypeDef",
    "DashboardSummaryTypeDef",
    "ListDashboardsResponseTypeDef",
    "GatewaySummaryTypeDef",
    "ListGatewaysResponseTypeDef",
    "PortalSummaryTypeDef",
    "ListPortalsResponseTypeDef",
    "ListProjectAssetsResponseTypeDef",
    "ProjectSummaryTypeDef",
    "ListProjectsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutAssetPropertyValueEntryTypeDef",
    "UpdateAssetModelResponseTypeDef",
    "UpdateAssetResponseTypeDef",
    "UpdateGatewayCapabilityConfigurationResponseTypeDef",
    "UpdatePortalResponseTypeDef",
    "WaiterConfigTypeDef",
)

AssetModelHierarchyDefinitionTypeDef = TypedDict(
    "AssetModelHierarchyDefinitionTypeDef", {"name": str, "childAssetModelId": str}
)

_RequiredAssetModelHierarchyTypeDef = TypedDict(
    "_RequiredAssetModelHierarchyTypeDef", {"name": str, "childAssetModelId": str}
)
_OptionalAssetModelHierarchyTypeDef = TypedDict(
    "_OptionalAssetModelHierarchyTypeDef", {"id": str}, total=False
)


class AssetModelHierarchyTypeDef(
    _RequiredAssetModelHierarchyTypeDef, _OptionalAssetModelHierarchyTypeDef
):
    pass


AttributeTypeDef = TypedDict("AttributeTypeDef", {"defaultValue": str}, total=False)

_RequiredVariableValueTypeDef = TypedDict("_RequiredVariableValueTypeDef", {"propertyId": str})
_OptionalVariableValueTypeDef = TypedDict(
    "_OptionalVariableValueTypeDef", {"hierarchyId": str}, total=False
)


class VariableValueTypeDef(_RequiredVariableValueTypeDef, _OptionalVariableValueTypeDef):
    pass


ExpressionVariableTypeDef = TypedDict(
    "ExpressionVariableTypeDef", {"name": str, "value": VariableValueTypeDef}
)

TumblingWindowTypeDef = TypedDict("TumblingWindowTypeDef", {"interval": str})

MetricWindowTypeDef = TypedDict(
    "MetricWindowTypeDef", {"tumbling": TumblingWindowTypeDef}, total=False
)

MetricTypeDef = TypedDict(
    "MetricTypeDef",
    {
        "expression": str,
        "variables": List[ExpressionVariableTypeDef],
        "window": MetricWindowTypeDef,
    },
)

TransformTypeDef = TypedDict(
    "TransformTypeDef", {"expression": str, "variables": List[ExpressionVariableTypeDef]}
)

PropertyTypeTypeDef = TypedDict(
    "PropertyTypeTypeDef",
    {
        "attribute": AttributeTypeDef,
        "measurement": Dict[str, Any],
        "transform": TransformTypeDef,
        "metric": MetricTypeDef,
    },
    total=False,
)

_RequiredAssetModelPropertyDefinitionTypeDef = TypedDict(
    "_RequiredAssetModelPropertyDefinitionTypeDef",
    {
        "name": str,
        "dataType": Literal["STRING", "INTEGER", "DOUBLE", "BOOLEAN"],
        "type": PropertyTypeTypeDef,
    },
)
_OptionalAssetModelPropertyDefinitionTypeDef = TypedDict(
    "_OptionalAssetModelPropertyDefinitionTypeDef", {"unit": str}, total=False
)


class AssetModelPropertyDefinitionTypeDef(
    _RequiredAssetModelPropertyDefinitionTypeDef, _OptionalAssetModelPropertyDefinitionTypeDef
):
    pass


_RequiredAssetModelPropertyTypeDef = TypedDict(
    "_RequiredAssetModelPropertyTypeDef",
    {
        "name": str,
        "dataType": Literal["STRING", "INTEGER", "DOUBLE", "BOOLEAN"],
        "type": PropertyTypeTypeDef,
    },
)
_OptionalAssetModelPropertyTypeDef = TypedDict(
    "_OptionalAssetModelPropertyTypeDef", {"id": str, "unit": str}, total=False
)


class AssetModelPropertyTypeDef(
    _RequiredAssetModelPropertyTypeDef, _OptionalAssetModelPropertyTypeDef
):
    pass


AssetErrorDetailsTypeDef = TypedDict(
    "AssetErrorDetailsTypeDef",
    {"assetId": str, "code": Literal["INTERNAL_FAILURE"], "message": str},
)

BatchAssociateProjectAssetsResponseTypeDef = TypedDict(
    "BatchAssociateProjectAssetsResponseTypeDef",
    {"errors": List[AssetErrorDetailsTypeDef]},
    total=False,
)

BatchDisassociateProjectAssetsResponseTypeDef = TypedDict(
    "BatchDisassociateProjectAssetsResponseTypeDef",
    {"errors": List[AssetErrorDetailsTypeDef]},
    total=False,
)

_RequiredTimeInNanosTypeDef = TypedDict("_RequiredTimeInNanosTypeDef", {"timeInSeconds": int})
_OptionalTimeInNanosTypeDef = TypedDict(
    "_OptionalTimeInNanosTypeDef", {"offsetInNanos": int}, total=False
)


class TimeInNanosTypeDef(_RequiredTimeInNanosTypeDef, _OptionalTimeInNanosTypeDef):
    pass


BatchPutAssetPropertyErrorTypeDef = TypedDict(
    "BatchPutAssetPropertyErrorTypeDef",
    {
        "errorCode": Literal[
            "ResourceNotFoundException",
            "InvalidRequestException",
            "InternalFailureException",
            "ServiceUnavailableException",
            "ThrottlingException",
            "LimitExceededException",
            "ConflictingOperationException",
            "TimestampOutOfRangeException",
            "AccessDeniedException",
        ],
        "errorMessage": str,
        "timestamps": List[TimeInNanosTypeDef],
    },
)

BatchPutAssetPropertyErrorEntryTypeDef = TypedDict(
    "BatchPutAssetPropertyErrorEntryTypeDef",
    {"entryId": str, "errors": List[BatchPutAssetPropertyErrorTypeDef]},
)

BatchPutAssetPropertyValueResponseTypeDef = TypedDict(
    "BatchPutAssetPropertyValueResponseTypeDef",
    {"errorEntries": List[BatchPutAssetPropertyErrorEntryTypeDef]},
)

CreateAccessPolicyResponseTypeDef = TypedDict(
    "CreateAccessPolicyResponseTypeDef", {"accessPolicyId": str, "accessPolicyArn": str}
)

ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef", {"code": Literal["VALIDATION_ERROR", "INTERNAL_FAILURE"], "message": str}
)

_RequiredAssetModelStatusTypeDef = TypedDict(
    "_RequiredAssetModelStatusTypeDef",
    {"state": Literal["CREATING", "ACTIVE", "UPDATING", "PROPAGATING", "DELETING", "FAILED"]},
)
_OptionalAssetModelStatusTypeDef = TypedDict(
    "_OptionalAssetModelStatusTypeDef", {"error": ErrorDetailsTypeDef}, total=False
)


class AssetModelStatusTypeDef(_RequiredAssetModelStatusTypeDef, _OptionalAssetModelStatusTypeDef):
    pass


CreateAssetModelResponseTypeDef = TypedDict(
    "CreateAssetModelResponseTypeDef",
    {"assetModelId": str, "assetModelArn": str, "assetModelStatus": AssetModelStatusTypeDef},
)

_RequiredAssetStatusTypeDef = TypedDict(
    "_RequiredAssetStatusTypeDef",
    {"state": Literal["CREATING", "ACTIVE", "UPDATING", "DELETING", "FAILED"]},
)
_OptionalAssetStatusTypeDef = TypedDict(
    "_OptionalAssetStatusTypeDef", {"error": ErrorDetailsTypeDef}, total=False
)


class AssetStatusTypeDef(_RequiredAssetStatusTypeDef, _OptionalAssetStatusTypeDef):
    pass


CreateAssetResponseTypeDef = TypedDict(
    "CreateAssetResponseTypeDef",
    {"assetId": str, "assetArn": str, "assetStatus": AssetStatusTypeDef},
)

CreateDashboardResponseTypeDef = TypedDict(
    "CreateDashboardResponseTypeDef", {"dashboardId": str, "dashboardArn": str}
)

CreateGatewayResponseTypeDef = TypedDict(
    "CreateGatewayResponseTypeDef", {"gatewayId": str, "gatewayArn": str}
)

MonitorErrorDetailsTypeDef = TypedDict(
    "MonitorErrorDetailsTypeDef", {"code": Literal["INTERNAL_FAILURE"], "message": str}, total=False
)

_RequiredPortalStatusTypeDef = TypedDict(
    "_RequiredPortalStatusTypeDef",
    {"state": Literal["CREATING", "UPDATING", "DELETING", "ACTIVE", "FAILED"]},
)
_OptionalPortalStatusTypeDef = TypedDict(
    "_OptionalPortalStatusTypeDef", {"error": MonitorErrorDetailsTypeDef}, total=False
)


class PortalStatusTypeDef(_RequiredPortalStatusTypeDef, _OptionalPortalStatusTypeDef):
    pass


CreatePortalResponseTypeDef = TypedDict(
    "CreatePortalResponseTypeDef",
    {
        "portalId": str,
        "portalArn": str,
        "portalStartUrl": str,
        "portalStatus": PortalStatusTypeDef,
        "ssoApplicationId": str,
    },
)

CreateProjectResponseTypeDef = TypedDict(
    "CreateProjectResponseTypeDef", {"projectId": str, "projectArn": str}
)

DeleteAssetModelResponseTypeDef = TypedDict(
    "DeleteAssetModelResponseTypeDef", {"assetModelStatus": AssetModelStatusTypeDef}
)

DeleteAssetResponseTypeDef = TypedDict(
    "DeleteAssetResponseTypeDef", {"assetStatus": AssetStatusTypeDef}
)

DeletePortalResponseTypeDef = TypedDict(
    "DeletePortalResponseTypeDef", {"portalStatus": PortalStatusTypeDef}
)

GroupIdentityTypeDef = TypedDict("GroupIdentityTypeDef", {"id": str})

UserIdentityTypeDef = TypedDict("UserIdentityTypeDef", {"id": str})

IdentityTypeDef = TypedDict(
    "IdentityTypeDef", {"user": UserIdentityTypeDef, "group": GroupIdentityTypeDef}, total=False
)

PortalResourceTypeDef = TypedDict("PortalResourceTypeDef", {"id": str})

ProjectResourceTypeDef = TypedDict("ProjectResourceTypeDef", {"id": str})

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {"portal": PortalResourceTypeDef, "project": ProjectResourceTypeDef},
    total=False,
)

DescribeAccessPolicyResponseTypeDef = TypedDict(
    "DescribeAccessPolicyResponseTypeDef",
    {
        "accessPolicyId": str,
        "accessPolicyArn": str,
        "accessPolicyIdentity": IdentityTypeDef,
        "accessPolicyResource": ResourceTypeDef,
        "accessPolicyPermission": Literal["ADMINISTRATOR", "VIEWER"],
        "accessPolicyCreationDate": datetime,
        "accessPolicyLastUpdateDate": datetime,
    },
)

DescribeAssetModelResponseTypeDef = TypedDict(
    "DescribeAssetModelResponseTypeDef",
    {
        "assetModelId": str,
        "assetModelArn": str,
        "assetModelName": str,
        "assetModelDescription": str,
        "assetModelProperties": List[AssetModelPropertyTypeDef],
        "assetModelHierarchies": List[AssetModelHierarchyTypeDef],
        "assetModelCreationDate": datetime,
        "assetModelLastUpdateDate": datetime,
        "assetModelStatus": AssetModelStatusTypeDef,
    },
)

PropertyNotificationTypeDef = TypedDict(
    "PropertyNotificationTypeDef", {"topic": str, "state": Literal["ENABLED", "DISABLED"]}
)

_RequiredPropertyTypeDef = TypedDict(
    "_RequiredPropertyTypeDef",
    {"id": str, "name": str, "dataType": Literal["STRING", "INTEGER", "DOUBLE", "BOOLEAN"]},
)
_OptionalPropertyTypeDef = TypedDict(
    "_OptionalPropertyTypeDef",
    {
        "alias": str,
        "notification": PropertyNotificationTypeDef,
        "unit": str,
        "type": PropertyTypeTypeDef,
    },
    total=False,
)


class PropertyTypeDef(_RequiredPropertyTypeDef, _OptionalPropertyTypeDef):
    pass


DescribeAssetPropertyResponseTypeDef = TypedDict(
    "DescribeAssetPropertyResponseTypeDef",
    {"assetId": str, "assetName": str, "assetModelId": str, "assetProperty": PropertyTypeDef},
)

_RequiredAssetHierarchyTypeDef = TypedDict("_RequiredAssetHierarchyTypeDef", {"name": str})
_OptionalAssetHierarchyTypeDef = TypedDict(
    "_OptionalAssetHierarchyTypeDef", {"id": str}, total=False
)


class AssetHierarchyTypeDef(_RequiredAssetHierarchyTypeDef, _OptionalAssetHierarchyTypeDef):
    pass


_RequiredAssetPropertyTypeDef = TypedDict(
    "_RequiredAssetPropertyTypeDef",
    {"id": str, "name": str, "dataType": Literal["STRING", "INTEGER", "DOUBLE", "BOOLEAN"]},
)
_OptionalAssetPropertyTypeDef = TypedDict(
    "_OptionalAssetPropertyTypeDef",
    {"alias": str, "notification": PropertyNotificationTypeDef, "unit": str},
    total=False,
)


class AssetPropertyTypeDef(_RequiredAssetPropertyTypeDef, _OptionalAssetPropertyTypeDef):
    pass


DescribeAssetResponseTypeDef = TypedDict(
    "DescribeAssetResponseTypeDef",
    {
        "assetId": str,
        "assetArn": str,
        "assetName": str,
        "assetModelId": str,
        "assetProperties": List[AssetPropertyTypeDef],
        "assetHierarchies": List[AssetHierarchyTypeDef],
        "assetCreationDate": datetime,
        "assetLastUpdateDate": datetime,
        "assetStatus": AssetStatusTypeDef,
    },
)

_RequiredDescribeDashboardResponseTypeDef = TypedDict(
    "_RequiredDescribeDashboardResponseTypeDef",
    {
        "dashboardId": str,
        "dashboardArn": str,
        "dashboardName": str,
        "projectId": str,
        "dashboardDefinition": str,
        "dashboardCreationDate": datetime,
        "dashboardLastUpdateDate": datetime,
    },
)
_OptionalDescribeDashboardResponseTypeDef = TypedDict(
    "_OptionalDescribeDashboardResponseTypeDef", {"dashboardDescription": str}, total=False
)


class DescribeDashboardResponseTypeDef(
    _RequiredDescribeDashboardResponseTypeDef, _OptionalDescribeDashboardResponseTypeDef
):
    pass


DescribeGatewayCapabilityConfigurationResponseTypeDef = TypedDict(
    "DescribeGatewayCapabilityConfigurationResponseTypeDef",
    {
        "gatewayId": str,
        "capabilityNamespace": str,
        "capabilityConfiguration": str,
        "capabilitySyncStatus": Literal["IN_SYNC", "OUT_OF_SYNC", "SYNC_FAILED"],
    },
)

GatewayCapabilitySummaryTypeDef = TypedDict(
    "GatewayCapabilitySummaryTypeDef",
    {
        "capabilityNamespace": str,
        "capabilitySyncStatus": Literal["IN_SYNC", "OUT_OF_SYNC", "SYNC_FAILED"],
    },
)

GreengrassTypeDef = TypedDict("GreengrassTypeDef", {"groupArn": str})

GatewayPlatformTypeDef = TypedDict("GatewayPlatformTypeDef", {"greengrass": GreengrassTypeDef})

_RequiredDescribeGatewayResponseTypeDef = TypedDict(
    "_RequiredDescribeGatewayResponseTypeDef",
    {
        "gatewayId": str,
        "gatewayName": str,
        "gatewayArn": str,
        "gatewayCapabilitySummaries": List[GatewayCapabilitySummaryTypeDef],
        "creationDate": datetime,
        "lastUpdateDate": datetime,
    },
)
_OptionalDescribeGatewayResponseTypeDef = TypedDict(
    "_OptionalDescribeGatewayResponseTypeDef",
    {"gatewayPlatform": GatewayPlatformTypeDef},
    total=False,
)


class DescribeGatewayResponseTypeDef(
    _RequiredDescribeGatewayResponseTypeDef, _OptionalDescribeGatewayResponseTypeDef
):
    pass


LoggingOptionsTypeDef = TypedDict(
    "LoggingOptionsTypeDef", {"level": Literal["ERROR", "INFO", "OFF"]}
)

DescribeLoggingOptionsResponseTypeDef = TypedDict(
    "DescribeLoggingOptionsResponseTypeDef", {"loggingOptions": LoggingOptionsTypeDef}
)

ImageTypeDef = TypedDict(
    "ImageTypeDef", {"locationUrl": str, "lastUpdateDate": datetime}, total=False
)

_RequiredDescribePortalResponseTypeDef = TypedDict(
    "_RequiredDescribePortalResponseTypeDef",
    {
        "portalId": str,
        "portalArn": str,
        "portalName": str,
        "portalClientId": str,
        "portalStartUrl": str,
        "portalContactEmail": str,
        "portalStatus": PortalStatusTypeDef,
        "portalCreationDate": datetime,
        "portalLastUpdateDate": datetime,
    },
)
_OptionalDescribePortalResponseTypeDef = TypedDict(
    "_OptionalDescribePortalResponseTypeDef",
    {"portalDescription": str, "portalLogoImage": ImageTypeDef, "roleArn": str},
    total=False,
)


class DescribePortalResponseTypeDef(
    _RequiredDescribePortalResponseTypeDef, _OptionalDescribePortalResponseTypeDef
):
    pass


_RequiredDescribeProjectResponseTypeDef = TypedDict(
    "_RequiredDescribeProjectResponseTypeDef",
    {
        "projectId": str,
        "projectArn": str,
        "projectName": str,
        "portalId": str,
        "projectCreationDate": datetime,
        "projectLastUpdateDate": datetime,
    },
)
_OptionalDescribeProjectResponseTypeDef = TypedDict(
    "_OptionalDescribeProjectResponseTypeDef", {"projectDescription": str}, total=False
)


class DescribeProjectResponseTypeDef(
    _RequiredDescribeProjectResponseTypeDef, _OptionalDescribeProjectResponseTypeDef
):
    pass


AggregatesTypeDef = TypedDict(
    "AggregatesTypeDef",
    {"average": float, "count": float, "maximum": float, "minimum": float, "sum": float},
    total=False,
)

_RequiredAggregatedValueTypeDef = TypedDict(
    "_RequiredAggregatedValueTypeDef", {"timestamp": datetime, "value": AggregatesTypeDef}
)
_OptionalAggregatedValueTypeDef = TypedDict(
    "_OptionalAggregatedValueTypeDef", {"quality": Literal["GOOD", "BAD", "UNCERTAIN"]}, total=False
)


class AggregatedValueTypeDef(_RequiredAggregatedValueTypeDef, _OptionalAggregatedValueTypeDef):
    pass


_RequiredGetAssetPropertyAggregatesResponseTypeDef = TypedDict(
    "_RequiredGetAssetPropertyAggregatesResponseTypeDef",
    {"aggregatedValues": List[AggregatedValueTypeDef]},
)
_OptionalGetAssetPropertyAggregatesResponseTypeDef = TypedDict(
    "_OptionalGetAssetPropertyAggregatesResponseTypeDef", {"nextToken": str}, total=False
)


class GetAssetPropertyAggregatesResponseTypeDef(
    _RequiredGetAssetPropertyAggregatesResponseTypeDef,
    _OptionalGetAssetPropertyAggregatesResponseTypeDef,
):
    pass


VariantTypeDef = TypedDict(
    "VariantTypeDef",
    {"stringValue": str, "integerValue": int, "doubleValue": float, "booleanValue": bool},
    total=False,
)

_RequiredAssetPropertyValueTypeDef = TypedDict(
    "_RequiredAssetPropertyValueTypeDef", {"value": VariantTypeDef, "timestamp": TimeInNanosTypeDef}
)
_OptionalAssetPropertyValueTypeDef = TypedDict(
    "_OptionalAssetPropertyValueTypeDef",
    {"quality": Literal["GOOD", "BAD", "UNCERTAIN"]},
    total=False,
)


class AssetPropertyValueTypeDef(
    _RequiredAssetPropertyValueTypeDef, _OptionalAssetPropertyValueTypeDef
):
    pass


_RequiredGetAssetPropertyValueHistoryResponseTypeDef = TypedDict(
    "_RequiredGetAssetPropertyValueHistoryResponseTypeDef",
    {"assetPropertyValueHistory": List[AssetPropertyValueTypeDef]},
)
_OptionalGetAssetPropertyValueHistoryResponseTypeDef = TypedDict(
    "_OptionalGetAssetPropertyValueHistoryResponseTypeDef", {"nextToken": str}, total=False
)


class GetAssetPropertyValueHistoryResponseTypeDef(
    _RequiredGetAssetPropertyValueHistoryResponseTypeDef,
    _OptionalGetAssetPropertyValueHistoryResponseTypeDef,
):
    pass


GetAssetPropertyValueResponseTypeDef = TypedDict(
    "GetAssetPropertyValueResponseTypeDef",
    {"propertyValue": AssetPropertyValueTypeDef},
    total=False,
)

ImageFileTypeDef = TypedDict(
    "ImageFileTypeDef", {"encodedString": Union[bytes, IO], "fileType": Literal["PNG"]}
)

_RequiredAccessPolicySummaryTypeDef = TypedDict(
    "_RequiredAccessPolicySummaryTypeDef",
    {
        "id": str,
        "identity": IdentityTypeDef,
        "resource": ResourceTypeDef,
        "permission": Literal["ADMINISTRATOR", "VIEWER"],
    },
)
_OptionalAccessPolicySummaryTypeDef = TypedDict(
    "_OptionalAccessPolicySummaryTypeDef",
    {"creationDate": datetime, "lastUpdateDate": datetime},
    total=False,
)


class AccessPolicySummaryTypeDef(
    _RequiredAccessPolicySummaryTypeDef, _OptionalAccessPolicySummaryTypeDef
):
    pass


_RequiredListAccessPoliciesResponseTypeDef = TypedDict(
    "_RequiredListAccessPoliciesResponseTypeDef",
    {"accessPolicySummaries": List[AccessPolicySummaryTypeDef]},
)
_OptionalListAccessPoliciesResponseTypeDef = TypedDict(
    "_OptionalListAccessPoliciesResponseTypeDef", {"nextToken": str}, total=False
)


class ListAccessPoliciesResponseTypeDef(
    _RequiredListAccessPoliciesResponseTypeDef, _OptionalListAccessPoliciesResponseTypeDef
):
    pass


AssetModelSummaryTypeDef = TypedDict(
    "AssetModelSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetModelStatusTypeDef,
    },
)

_RequiredListAssetModelsResponseTypeDef = TypedDict(
    "_RequiredListAssetModelsResponseTypeDef",
    {"assetModelSummaries": List[AssetModelSummaryTypeDef]},
)
_OptionalListAssetModelsResponseTypeDef = TypedDict(
    "_OptionalListAssetModelsResponseTypeDef", {"nextToken": str}, total=False
)


class ListAssetModelsResponseTypeDef(
    _RequiredListAssetModelsResponseTypeDef, _OptionalListAssetModelsResponseTypeDef
):
    pass


AssetSummaryTypeDef = TypedDict(
    "AssetSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetStatusTypeDef,
        "hierarchies": List[AssetHierarchyTypeDef],
    },
)

_RequiredListAssetsResponseTypeDef = TypedDict(
    "_RequiredListAssetsResponseTypeDef", {"assetSummaries": List[AssetSummaryTypeDef]}
)
_OptionalListAssetsResponseTypeDef = TypedDict(
    "_OptionalListAssetsResponseTypeDef", {"nextToken": str}, total=False
)


class ListAssetsResponseTypeDef(
    _RequiredListAssetsResponseTypeDef, _OptionalListAssetsResponseTypeDef
):
    pass


AssociatedAssetsSummaryTypeDef = TypedDict(
    "AssociatedAssetsSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetStatusTypeDef,
        "hierarchies": List[AssetHierarchyTypeDef],
    },
)

_RequiredListAssociatedAssetsResponseTypeDef = TypedDict(
    "_RequiredListAssociatedAssetsResponseTypeDef",
    {"assetSummaries": List[AssociatedAssetsSummaryTypeDef]},
)
_OptionalListAssociatedAssetsResponseTypeDef = TypedDict(
    "_OptionalListAssociatedAssetsResponseTypeDef", {"nextToken": str}, total=False
)


class ListAssociatedAssetsResponseTypeDef(
    _RequiredListAssociatedAssetsResponseTypeDef, _OptionalListAssociatedAssetsResponseTypeDef
):
    pass


_RequiredDashboardSummaryTypeDef = TypedDict(
    "_RequiredDashboardSummaryTypeDef", {"id": str, "name": str}
)
_OptionalDashboardSummaryTypeDef = TypedDict(
    "_OptionalDashboardSummaryTypeDef",
    {"description": str, "creationDate": datetime, "lastUpdateDate": datetime},
    total=False,
)


class DashboardSummaryTypeDef(_RequiredDashboardSummaryTypeDef, _OptionalDashboardSummaryTypeDef):
    pass


_RequiredListDashboardsResponseTypeDef = TypedDict(
    "_RequiredListDashboardsResponseTypeDef", {"dashboardSummaries": List[DashboardSummaryTypeDef]}
)
_OptionalListDashboardsResponseTypeDef = TypedDict(
    "_OptionalListDashboardsResponseTypeDef", {"nextToken": str}, total=False
)


class ListDashboardsResponseTypeDef(
    _RequiredListDashboardsResponseTypeDef, _OptionalListDashboardsResponseTypeDef
):
    pass


_RequiredGatewaySummaryTypeDef = TypedDict(
    "_RequiredGatewaySummaryTypeDef",
    {"gatewayId": str, "gatewayName": str, "creationDate": datetime, "lastUpdateDate": datetime},
)
_OptionalGatewaySummaryTypeDef = TypedDict(
    "_OptionalGatewaySummaryTypeDef",
    {"gatewayCapabilitySummaries": List[GatewayCapabilitySummaryTypeDef]},
    total=False,
)


class GatewaySummaryTypeDef(_RequiredGatewaySummaryTypeDef, _OptionalGatewaySummaryTypeDef):
    pass


_RequiredListGatewaysResponseTypeDef = TypedDict(
    "_RequiredListGatewaysResponseTypeDef", {"gatewaySummaries": List[GatewaySummaryTypeDef]}
)
_OptionalListGatewaysResponseTypeDef = TypedDict(
    "_OptionalListGatewaysResponseTypeDef", {"nextToken": str}, total=False
)


class ListGatewaysResponseTypeDef(
    _RequiredListGatewaysResponseTypeDef, _OptionalListGatewaysResponseTypeDef
):
    pass


_RequiredPortalSummaryTypeDef = TypedDict(
    "_RequiredPortalSummaryTypeDef", {"id": str, "name": str, "startUrl": str}
)
_OptionalPortalSummaryTypeDef = TypedDict(
    "_OptionalPortalSummaryTypeDef",
    {"description": str, "creationDate": datetime, "lastUpdateDate": datetime, "roleArn": str},
    total=False,
)


class PortalSummaryTypeDef(_RequiredPortalSummaryTypeDef, _OptionalPortalSummaryTypeDef):
    pass


ListPortalsResponseTypeDef = TypedDict(
    "ListPortalsResponseTypeDef",
    {"portalSummaries": List[PortalSummaryTypeDef], "nextToken": str},
    total=False,
)

_RequiredListProjectAssetsResponseTypeDef = TypedDict(
    "_RequiredListProjectAssetsResponseTypeDef", {"assetIds": List[str]}
)
_OptionalListProjectAssetsResponseTypeDef = TypedDict(
    "_OptionalListProjectAssetsResponseTypeDef", {"nextToken": str}, total=False
)


class ListProjectAssetsResponseTypeDef(
    _RequiredListProjectAssetsResponseTypeDef, _OptionalListProjectAssetsResponseTypeDef
):
    pass


_RequiredProjectSummaryTypeDef = TypedDict(
    "_RequiredProjectSummaryTypeDef", {"id": str, "name": str}
)
_OptionalProjectSummaryTypeDef = TypedDict(
    "_OptionalProjectSummaryTypeDef",
    {"description": str, "creationDate": datetime, "lastUpdateDate": datetime},
    total=False,
)


class ProjectSummaryTypeDef(_RequiredProjectSummaryTypeDef, _OptionalProjectSummaryTypeDef):
    pass


_RequiredListProjectsResponseTypeDef = TypedDict(
    "_RequiredListProjectsResponseTypeDef", {"projectSummaries": List[ProjectSummaryTypeDef]}
)
_OptionalListProjectsResponseTypeDef = TypedDict(
    "_OptionalListProjectsResponseTypeDef", {"nextToken": str}, total=False
)


class ListProjectsResponseTypeDef(
    _RequiredListProjectsResponseTypeDef, _OptionalListProjectsResponseTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": Dict[str, str]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

_RequiredPutAssetPropertyValueEntryTypeDef = TypedDict(
    "_RequiredPutAssetPropertyValueEntryTypeDef",
    {"entryId": str, "propertyValues": List[AssetPropertyValueTypeDef]},
)
_OptionalPutAssetPropertyValueEntryTypeDef = TypedDict(
    "_OptionalPutAssetPropertyValueEntryTypeDef",
    {"assetId": str, "propertyId": str, "propertyAlias": str},
    total=False,
)


class PutAssetPropertyValueEntryTypeDef(
    _RequiredPutAssetPropertyValueEntryTypeDef, _OptionalPutAssetPropertyValueEntryTypeDef
):
    pass


UpdateAssetModelResponseTypeDef = TypedDict(
    "UpdateAssetModelResponseTypeDef", {"assetModelStatus": AssetModelStatusTypeDef}
)

UpdateAssetResponseTypeDef = TypedDict(
    "UpdateAssetResponseTypeDef", {"assetStatus": AssetStatusTypeDef}
)

UpdateGatewayCapabilityConfigurationResponseTypeDef = TypedDict(
    "UpdateGatewayCapabilityConfigurationResponseTypeDef",
    {
        "capabilityNamespace": str,
        "capabilitySyncStatus": Literal["IN_SYNC", "OUT_OF_SYNC", "SYNC_FAILED"],
    },
)

UpdatePortalResponseTypeDef = TypedDict(
    "UpdatePortalResponseTypeDef", {"portalStatus": PortalStatusTypeDef}
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
