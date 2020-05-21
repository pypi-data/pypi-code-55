"""
Main interface for kendra service type definitions.

Usage::

    from mypy_boto3.kendra.type_defs import DocumentAttributeValueTypeDef

    data: DocumentAttributeValueTypeDef = {...}
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
    "DocumentAttributeValueTypeDef",
    "DocumentAttributeTypeDef",
    "AttributeFilterTypeDef",
    "BatchDeleteDocumentResponseFailedDocumentTypeDef",
    "BatchDeleteDocumentResponseTypeDef",
    "BatchPutDocumentResponseFailedDocumentTypeDef",
    "BatchPutDocumentResponseTypeDef",
    "CapacityUnitsConfigurationTypeDef",
    "ClickFeedbackTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateFaqResponseTypeDef",
    "CreateIndexResponseTypeDef",
    "AclConfigurationTypeDef",
    "DataSourceToIndexFieldMappingTypeDef",
    "ColumnConfigurationTypeDef",
    "ConnectionConfigurationTypeDef",
    "DataSourceVpcConfigurationTypeDef",
    "DatabaseConfigurationTypeDef",
    "S3PathTypeDef",
    "OneDriveUsersTypeDef",
    "OneDriveConfigurationTypeDef",
    "AccessControlListConfigurationTypeDef",
    "DocumentsMetadataConfigurationTypeDef",
    "S3DataSourceConfigurationTypeDef",
    "SalesforceChatterFeedConfigurationTypeDef",
    "SalesforceCustomKnowledgeArticleTypeConfigurationTypeDef",
    "SalesforceStandardKnowledgeArticleTypeConfigurationTypeDef",
    "SalesforceKnowledgeArticleConfigurationTypeDef",
    "SalesforceStandardObjectAttachmentConfigurationTypeDef",
    "SalesforceStandardObjectConfigurationTypeDef",
    "SalesforceConfigurationTypeDef",
    "ServiceNowKnowledgeArticleConfigurationTypeDef",
    "ServiceNowServiceCatalogConfigurationTypeDef",
    "ServiceNowConfigurationTypeDef",
    "SharePointConfigurationTypeDef",
    "DataSourceConfigurationTypeDef",
    "DataSourceSyncJobMetricTargetTypeDef",
    "DescribeDataSourceResponseTypeDef",
    "DescribeFaqResponseTypeDef",
    "RelevanceTypeDef",
    "SearchTypeDef",
    "DocumentMetadataConfigurationTypeDef",
    "FaqStatisticsTypeDef",
    "TextDocumentStatisticsTypeDef",
    "IndexStatisticsTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "DescribeIndexResponseTypeDef",
    "PrincipalTypeDef",
    "DocumentTypeDef",
    "FacetTypeDef",
    "DataSourceSyncJobMetricsTypeDef",
    "DataSourceSyncJobTypeDef",
    "ListDataSourceSyncJobsResponseTypeDef",
    "DataSourceSummaryTypeDef",
    "ListDataSourcesResponseTypeDef",
    "FaqSummaryTypeDef",
    "ListFaqsResponseTypeDef",
    "IndexConfigurationSummaryTypeDef",
    "ListIndicesResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "DocumentAttributeValueCountPairTypeDef",
    "FacetResultTypeDef",
    "HighlightTypeDef",
    "TextWithHighlightsTypeDef",
    "AdditionalResultAttributeValueTypeDef",
    "AdditionalResultAttributeTypeDef",
    "QueryResultItemTypeDef",
    "QueryResultTypeDef",
    "RelevanceFeedbackTypeDef",
    "StartDataSourceSyncJobResponseTypeDef",
    "TimeRangeTypeDef",
)

DocumentAttributeValueTypeDef = TypedDict(
    "DocumentAttributeValueTypeDef",
    {"StringValue": str, "StringListValue": List[str], "LongValue": int, "DateValue": datetime},
    total=False,
)

DocumentAttributeTypeDef = TypedDict(
    "DocumentAttributeTypeDef", {"Key": str, "Value": DocumentAttributeValueTypeDef}
)

AttributeFilterTypeDef = TypedDict(
    "AttributeFilterTypeDef",
    {
        "AndAllFilters": List["AttributeFilterTypeDef"],
        "OrAllFilters": List["AttributeFilterTypeDef"],
        "NotFilter": "AttributeFilterTypeDef",
        "EqualsTo": DocumentAttributeTypeDef,
        "ContainsAll": DocumentAttributeTypeDef,
        "ContainsAny": DocumentAttributeTypeDef,
        "GreaterThan": DocumentAttributeTypeDef,
        "GreaterThanOrEquals": DocumentAttributeTypeDef,
        "LessThan": DocumentAttributeTypeDef,
        "LessThanOrEquals": DocumentAttributeTypeDef,
    },
    total=False,
)

BatchDeleteDocumentResponseFailedDocumentTypeDef = TypedDict(
    "BatchDeleteDocumentResponseFailedDocumentTypeDef",
    {"Id": str, "ErrorCode": Literal["InternalError", "InvalidRequest"], "ErrorMessage": str},
    total=False,
)

BatchDeleteDocumentResponseTypeDef = TypedDict(
    "BatchDeleteDocumentResponseTypeDef",
    {"FailedDocuments": List[BatchDeleteDocumentResponseFailedDocumentTypeDef]},
    total=False,
)

BatchPutDocumentResponseFailedDocumentTypeDef = TypedDict(
    "BatchPutDocumentResponseFailedDocumentTypeDef",
    {"Id": str, "ErrorCode": Literal["InternalError", "InvalidRequest"], "ErrorMessage": str},
    total=False,
)

BatchPutDocumentResponseTypeDef = TypedDict(
    "BatchPutDocumentResponseTypeDef",
    {"FailedDocuments": List[BatchPutDocumentResponseFailedDocumentTypeDef]},
    total=False,
)

CapacityUnitsConfigurationTypeDef = TypedDict(
    "CapacityUnitsConfigurationTypeDef", {"StorageCapacityUnits": int, "QueryCapacityUnits": int}
)

ClickFeedbackTypeDef = TypedDict("ClickFeedbackTypeDef", {"ResultId": str, "ClickTime": datetime})

CreateDataSourceResponseTypeDef = TypedDict("CreateDataSourceResponseTypeDef", {"Id": str})

CreateFaqResponseTypeDef = TypedDict("CreateFaqResponseTypeDef", {"Id": str}, total=False)

CreateIndexResponseTypeDef = TypedDict("CreateIndexResponseTypeDef", {"Id": str}, total=False)

AclConfigurationTypeDef = TypedDict("AclConfigurationTypeDef", {"AllowedGroupsColumnName": str})

_RequiredDataSourceToIndexFieldMappingTypeDef = TypedDict(
    "_RequiredDataSourceToIndexFieldMappingTypeDef",
    {"DataSourceFieldName": str, "IndexFieldName": str},
)
_OptionalDataSourceToIndexFieldMappingTypeDef = TypedDict(
    "_OptionalDataSourceToIndexFieldMappingTypeDef", {"DateFieldFormat": str}, total=False
)


class DataSourceToIndexFieldMappingTypeDef(
    _RequiredDataSourceToIndexFieldMappingTypeDef, _OptionalDataSourceToIndexFieldMappingTypeDef
):
    pass


_RequiredColumnConfigurationTypeDef = TypedDict(
    "_RequiredColumnConfigurationTypeDef",
    {
        "DocumentIdColumnName": str,
        "DocumentDataColumnName": str,
        "ChangeDetectingColumns": List[str],
    },
)
_OptionalColumnConfigurationTypeDef = TypedDict(
    "_OptionalColumnConfigurationTypeDef",
    {"DocumentTitleColumnName": str, "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef]},
    total=False,
)


class ColumnConfigurationTypeDef(
    _RequiredColumnConfigurationTypeDef, _OptionalColumnConfigurationTypeDef
):
    pass


ConnectionConfigurationTypeDef = TypedDict(
    "ConnectionConfigurationTypeDef",
    {
        "DatabaseHost": str,
        "DatabasePort": int,
        "DatabaseName": str,
        "TableName": str,
        "SecretArn": str,
    },
)

DataSourceVpcConfigurationTypeDef = TypedDict(
    "DataSourceVpcConfigurationTypeDef", {"SubnetIds": List[str], "SecurityGroupIds": List[str]}
)

_RequiredDatabaseConfigurationTypeDef = TypedDict(
    "_RequiredDatabaseConfigurationTypeDef",
    {
        "DatabaseEngineType": Literal[
            "RDS_AURORA_MYSQL", "RDS_AURORA_POSTGRESQL", "RDS_MYSQL", "RDS_POSTGRESQL"
        ],
        "ConnectionConfiguration": ConnectionConfigurationTypeDef,
        "ColumnConfiguration": ColumnConfigurationTypeDef,
    },
)
_OptionalDatabaseConfigurationTypeDef = TypedDict(
    "_OptionalDatabaseConfigurationTypeDef",
    {
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
        "AclConfiguration": AclConfigurationTypeDef,
    },
    total=False,
)


class DatabaseConfigurationTypeDef(
    _RequiredDatabaseConfigurationTypeDef, _OptionalDatabaseConfigurationTypeDef
):
    pass


S3PathTypeDef = TypedDict("S3PathTypeDef", {"Bucket": str, "Key": str})

OneDriveUsersTypeDef = TypedDict(
    "OneDriveUsersTypeDef",
    {"OneDriveUserList": List[str], "OneDriveUserS3Path": S3PathTypeDef},
    total=False,
)

_RequiredOneDriveConfigurationTypeDef = TypedDict(
    "_RequiredOneDriveConfigurationTypeDef",
    {"TenantDomain": str, "SecretArn": str, "OneDriveUsers": OneDriveUsersTypeDef},
)
_OptionalOneDriveConfigurationTypeDef = TypedDict(
    "_OptionalOneDriveConfigurationTypeDef",
    {
        "InclusionPatterns": List[str],
        "ExclusionPatterns": List[str],
        "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)


class OneDriveConfigurationTypeDef(
    _RequiredOneDriveConfigurationTypeDef, _OptionalOneDriveConfigurationTypeDef
):
    pass


AccessControlListConfigurationTypeDef = TypedDict(
    "AccessControlListConfigurationTypeDef", {"KeyPath": str}, total=False
)

DocumentsMetadataConfigurationTypeDef = TypedDict(
    "DocumentsMetadataConfigurationTypeDef", {"S3Prefix": str}, total=False
)

_RequiredS3DataSourceConfigurationTypeDef = TypedDict(
    "_RequiredS3DataSourceConfigurationTypeDef", {"BucketName": str}
)
_OptionalS3DataSourceConfigurationTypeDef = TypedDict(
    "_OptionalS3DataSourceConfigurationTypeDef",
    {
        "InclusionPrefixes": List[str],
        "ExclusionPatterns": List[str],
        "DocumentsMetadataConfiguration": DocumentsMetadataConfigurationTypeDef,
        "AccessControlListConfiguration": AccessControlListConfigurationTypeDef,
    },
    total=False,
)


class S3DataSourceConfigurationTypeDef(
    _RequiredS3DataSourceConfigurationTypeDef, _OptionalS3DataSourceConfigurationTypeDef
):
    pass


_RequiredSalesforceChatterFeedConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceChatterFeedConfigurationTypeDef", {"DocumentDataFieldName": str}
)
_OptionalSalesforceChatterFeedConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceChatterFeedConfigurationTypeDef",
    {
        "DocumentTitleFieldName": str,
        "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef],
        "IncludeFilterTypes": List[Literal["ACTIVE_USER", "STANDARD_USER"]],
    },
    total=False,
)


class SalesforceChatterFeedConfigurationTypeDef(
    _RequiredSalesforceChatterFeedConfigurationTypeDef,
    _OptionalSalesforceChatterFeedConfigurationTypeDef,
):
    pass


_RequiredSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef",
    {"Name": str, "DocumentDataFieldName": str},
)
_OptionalSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef",
    {"DocumentTitleFieldName": str, "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef]},
    total=False,
)


class SalesforceCustomKnowledgeArticleTypeConfigurationTypeDef(
    _RequiredSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef,
    _OptionalSalesforceCustomKnowledgeArticleTypeConfigurationTypeDef,
):
    pass


_RequiredSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef",
    {"DocumentDataFieldName": str},
)
_OptionalSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef",
    {"DocumentTitleFieldName": str, "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef]},
    total=False,
)


class SalesforceStandardKnowledgeArticleTypeConfigurationTypeDef(
    _RequiredSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef,
    _OptionalSalesforceStandardKnowledgeArticleTypeConfigurationTypeDef,
):
    pass


_RequiredSalesforceKnowledgeArticleConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceKnowledgeArticleConfigurationTypeDef",
    {"IncludedStates": List[Literal["DRAFT", "PUBLISHED", "ARCHIVED"]]},
)
_OptionalSalesforceKnowledgeArticleConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceKnowledgeArticleConfigurationTypeDef",
    {
        "StandardKnowledgeArticleTypeConfiguration": SalesforceStandardKnowledgeArticleTypeConfigurationTypeDef,
        "CustomKnowledgeArticleTypeConfigurations": List[
            SalesforceCustomKnowledgeArticleTypeConfigurationTypeDef
        ],
    },
    total=False,
)


class SalesforceKnowledgeArticleConfigurationTypeDef(
    _RequiredSalesforceKnowledgeArticleConfigurationTypeDef,
    _OptionalSalesforceKnowledgeArticleConfigurationTypeDef,
):
    pass


SalesforceStandardObjectAttachmentConfigurationTypeDef = TypedDict(
    "SalesforceStandardObjectAttachmentConfigurationTypeDef",
    {"DocumentTitleFieldName": str, "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef]},
    total=False,
)

_RequiredSalesforceStandardObjectConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceStandardObjectConfigurationTypeDef",
    {
        "Name": Literal[
            "ACCOUNT",
            "CAMPAIGN",
            "CASE",
            "CONTACT",
            "CONTRACT",
            "DOCUMENT",
            "GROUP",
            "IDEA",
            "LEAD",
            "OPPORTUNITY",
            "PARTNER",
            "PRICEBOOK",
            "PRODUCT",
            "PROFILE",
            "SOLUTION",
            "TASK",
            "USER",
        ],
        "DocumentDataFieldName": str,
    },
)
_OptionalSalesforceStandardObjectConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceStandardObjectConfigurationTypeDef",
    {"DocumentTitleFieldName": str, "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef]},
    total=False,
)


class SalesforceStandardObjectConfigurationTypeDef(
    _RequiredSalesforceStandardObjectConfigurationTypeDef,
    _OptionalSalesforceStandardObjectConfigurationTypeDef,
):
    pass


_RequiredSalesforceConfigurationTypeDef = TypedDict(
    "_RequiredSalesforceConfigurationTypeDef", {"ServerUrl": str, "SecretArn": str}
)
_OptionalSalesforceConfigurationTypeDef = TypedDict(
    "_OptionalSalesforceConfigurationTypeDef",
    {
        "StandardObjectConfigurations": List[SalesforceStandardObjectConfigurationTypeDef],
        "KnowledgeArticleConfiguration": SalesforceKnowledgeArticleConfigurationTypeDef,
        "ChatterFeedConfiguration": SalesforceChatterFeedConfigurationTypeDef,
        "CrawlAttachments": bool,
        "StandardObjectAttachmentConfiguration": SalesforceStandardObjectAttachmentConfigurationTypeDef,
        "IncludeAttachmentFilePatterns": List[str],
        "ExcludeAttachmentFilePatterns": List[str],
    },
    total=False,
)


class SalesforceConfigurationTypeDef(
    _RequiredSalesforceConfigurationTypeDef, _OptionalSalesforceConfigurationTypeDef
):
    pass


_RequiredServiceNowKnowledgeArticleConfigurationTypeDef = TypedDict(
    "_RequiredServiceNowKnowledgeArticleConfigurationTypeDef", {"DocumentDataFieldName": str}
)
_OptionalServiceNowKnowledgeArticleConfigurationTypeDef = TypedDict(
    "_OptionalServiceNowKnowledgeArticleConfigurationTypeDef",
    {
        "CrawlAttachments": bool,
        "IncludeAttachmentFilePatterns": List[str],
        "ExcludeAttachmentFilePatterns": List[str],
        "DocumentTitleFieldName": str,
        "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)


class ServiceNowKnowledgeArticleConfigurationTypeDef(
    _RequiredServiceNowKnowledgeArticleConfigurationTypeDef,
    _OptionalServiceNowKnowledgeArticleConfigurationTypeDef,
):
    pass


_RequiredServiceNowServiceCatalogConfigurationTypeDef = TypedDict(
    "_RequiredServiceNowServiceCatalogConfigurationTypeDef", {"DocumentDataFieldName": str}
)
_OptionalServiceNowServiceCatalogConfigurationTypeDef = TypedDict(
    "_OptionalServiceNowServiceCatalogConfigurationTypeDef",
    {
        "CrawlAttachments": bool,
        "IncludeAttachmentFilePatterns": List[str],
        "ExcludeAttachmentFilePatterns": List[str],
        "DocumentTitleFieldName": str,
        "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef],
    },
    total=False,
)


class ServiceNowServiceCatalogConfigurationTypeDef(
    _RequiredServiceNowServiceCatalogConfigurationTypeDef,
    _OptionalServiceNowServiceCatalogConfigurationTypeDef,
):
    pass


_RequiredServiceNowConfigurationTypeDef = TypedDict(
    "_RequiredServiceNowConfigurationTypeDef",
    {"HostUrl": str, "SecretArn": str, "ServiceNowBuildVersion": Literal["LONDON", "OTHERS"]},
)
_OptionalServiceNowConfigurationTypeDef = TypedDict(
    "_OptionalServiceNowConfigurationTypeDef",
    {
        "KnowledgeArticleConfiguration": ServiceNowKnowledgeArticleConfigurationTypeDef,
        "ServiceCatalogConfiguration": ServiceNowServiceCatalogConfigurationTypeDef,
    },
    total=False,
)


class ServiceNowConfigurationTypeDef(
    _RequiredServiceNowConfigurationTypeDef, _OptionalServiceNowConfigurationTypeDef
):
    pass


_RequiredSharePointConfigurationTypeDef = TypedDict(
    "_RequiredSharePointConfigurationTypeDef",
    {"SharePointVersion": Literal["SHAREPOINT_ONLINE"], "Urls": List[str], "SecretArn": str},
)
_OptionalSharePointConfigurationTypeDef = TypedDict(
    "_OptionalSharePointConfigurationTypeDef",
    {
        "CrawlAttachments": bool,
        "UseChangeLog": bool,
        "InclusionPatterns": List[str],
        "ExclusionPatterns": List[str],
        "VpcConfiguration": DataSourceVpcConfigurationTypeDef,
        "FieldMappings": List[DataSourceToIndexFieldMappingTypeDef],
        "DocumentTitleFieldName": str,
    },
    total=False,
)


class SharePointConfigurationTypeDef(
    _RequiredSharePointConfigurationTypeDef, _OptionalSharePointConfigurationTypeDef
):
    pass


DataSourceConfigurationTypeDef = TypedDict(
    "DataSourceConfigurationTypeDef",
    {
        "S3Configuration": S3DataSourceConfigurationTypeDef,
        "SharePointConfiguration": SharePointConfigurationTypeDef,
        "DatabaseConfiguration": DatabaseConfigurationTypeDef,
        "SalesforceConfiguration": SalesforceConfigurationTypeDef,
        "OneDriveConfiguration": OneDriveConfigurationTypeDef,
        "ServiceNowConfiguration": ServiceNowConfigurationTypeDef,
    },
    total=False,
)

DataSourceSyncJobMetricTargetTypeDef = TypedDict(
    "DataSourceSyncJobMetricTargetTypeDef", {"DataSourceId": str, "DataSourceSyncJobId": str}
)

DescribeDataSourceResponseTypeDef = TypedDict(
    "DescribeDataSourceResponseTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "Name": str,
        "Type": Literal["S3", "SHAREPOINT", "DATABASE", "SALESFORCE", "ONEDRIVE", "SERVICENOW"],
        "Configuration": DataSourceConfigurationTypeDef,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Description": str,
        "Status": Literal["CREATING", "DELETING", "FAILED", "UPDATING", "ACTIVE"],
        "Schedule": str,
        "RoleArn": str,
        "ErrorMessage": str,
    },
    total=False,
)

DescribeFaqResponseTypeDef = TypedDict(
    "DescribeFaqResponseTypeDef",
    {
        "Id": str,
        "IndexId": str,
        "Name": str,
        "Description": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "S3Path": S3PathTypeDef,
        "Status": Literal["CREATING", "UPDATING", "ACTIVE", "DELETING", "FAILED"],
        "RoleArn": str,
        "ErrorMessage": str,
    },
    total=False,
)

RelevanceTypeDef = TypedDict(
    "RelevanceTypeDef",
    {
        "Freshness": bool,
        "Importance": int,
        "Duration": str,
        "RankOrder": Literal["ASCENDING", "DESCENDING"],
        "ValueImportanceMap": Dict[str, int],
    },
    total=False,
)

SearchTypeDef = TypedDict(
    "SearchTypeDef", {"Facetable": bool, "Searchable": bool, "Displayable": bool}, total=False
)

_RequiredDocumentMetadataConfigurationTypeDef = TypedDict(
    "_RequiredDocumentMetadataConfigurationTypeDef",
    {"Name": str, "Type": Literal["STRING_VALUE", "STRING_LIST_VALUE", "LONG_VALUE", "DATE_VALUE"]},
)
_OptionalDocumentMetadataConfigurationTypeDef = TypedDict(
    "_OptionalDocumentMetadataConfigurationTypeDef",
    {"Relevance": RelevanceTypeDef, "Search": SearchTypeDef},
    total=False,
)


class DocumentMetadataConfigurationTypeDef(
    _RequiredDocumentMetadataConfigurationTypeDef, _OptionalDocumentMetadataConfigurationTypeDef
):
    pass


FaqStatisticsTypeDef = TypedDict("FaqStatisticsTypeDef", {"IndexedQuestionAnswersCount": int})

TextDocumentStatisticsTypeDef = TypedDict(
    "TextDocumentStatisticsTypeDef", {"IndexedTextDocumentsCount": int, "IndexedTextBytes": int}
)

IndexStatisticsTypeDef = TypedDict(
    "IndexStatisticsTypeDef",
    {
        "FaqStatistics": FaqStatisticsTypeDef,
        "TextDocumentStatistics": TextDocumentStatisticsTypeDef,
    },
)

ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef", {"KmsKeyId": str}, total=False
)

DescribeIndexResponseTypeDef = TypedDict(
    "DescribeIndexResponseTypeDef",
    {
        "Name": str,
        "Id": str,
        "Edition": Literal["DEVELOPER_EDITION", "ENTERPRISE_EDITION"],
        "RoleArn": str,
        "ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "Status": Literal[
            "CREATING", "ACTIVE", "DELETING", "FAILED", "UPDATING", "SYSTEM_UPDATING"
        ],
        "Description": str,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "DocumentMetadataConfigurations": List[DocumentMetadataConfigurationTypeDef],
        "IndexStatistics": IndexStatisticsTypeDef,
        "ErrorMessage": str,
        "CapacityUnits": CapacityUnitsConfigurationTypeDef,
    },
    total=False,
)

PrincipalTypeDef = TypedDict(
    "PrincipalTypeDef",
    {"Name": str, "Type": Literal["USER", "GROUP"], "Access": Literal["ALLOW", "DENY"]},
)

_RequiredDocumentTypeDef = TypedDict("_RequiredDocumentTypeDef", {"Id": str})
_OptionalDocumentTypeDef = TypedDict(
    "_OptionalDocumentTypeDef",
    {
        "Title": str,
        "Blob": Union[bytes, IO],
        "S3Path": S3PathTypeDef,
        "Attributes": List[DocumentAttributeTypeDef],
        "AccessControlList": List[PrincipalTypeDef],
        "ContentType": Literal["PDF", "HTML", "MS_WORD", "PLAIN_TEXT", "PPT"],
    },
    total=False,
)


class DocumentTypeDef(_RequiredDocumentTypeDef, _OptionalDocumentTypeDef):
    pass


FacetTypeDef = TypedDict("FacetTypeDef", {"DocumentAttributeKey": str}, total=False)

DataSourceSyncJobMetricsTypeDef = TypedDict(
    "DataSourceSyncJobMetricsTypeDef",
    {
        "DocumentsAdded": str,
        "DocumentsModified": str,
        "DocumentsDeleted": str,
        "DocumentsFailed": str,
        "DocumentsScanned": str,
    },
    total=False,
)

DataSourceSyncJobTypeDef = TypedDict(
    "DataSourceSyncJobTypeDef",
    {
        "ExecutionId": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "Status": Literal[
            "FAILED",
            "SUCCEEDED",
            "SYNCING",
            "INCOMPLETE",
            "STOPPING",
            "ABORTED",
            "SYNCING_INDEXING",
        ],
        "ErrorMessage": str,
        "ErrorCode": Literal["InternalError", "InvalidRequest"],
        "DataSourceErrorCode": str,
        "Metrics": DataSourceSyncJobMetricsTypeDef,
    },
    total=False,
)

ListDataSourceSyncJobsResponseTypeDef = TypedDict(
    "ListDataSourceSyncJobsResponseTypeDef",
    {"History": List[DataSourceSyncJobTypeDef], "NextToken": str},
    total=False,
)

DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "Type": Literal["S3", "SHAREPOINT", "DATABASE", "SALESFORCE", "ONEDRIVE", "SERVICENOW"],
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Status": Literal["CREATING", "DELETING", "FAILED", "UPDATING", "ACTIVE"],
    },
    total=False,
)

ListDataSourcesResponseTypeDef = TypedDict(
    "ListDataSourcesResponseTypeDef",
    {"SummaryItems": List[DataSourceSummaryTypeDef], "NextToken": str},
    total=False,
)

FaqSummaryTypeDef = TypedDict(
    "FaqSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Status": Literal["CREATING", "UPDATING", "ACTIVE", "DELETING", "FAILED"],
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
    },
    total=False,
)

ListFaqsResponseTypeDef = TypedDict(
    "ListFaqsResponseTypeDef",
    {"NextToken": str, "FaqSummaryItems": List[FaqSummaryTypeDef]},
    total=False,
)

_RequiredIndexConfigurationSummaryTypeDef = TypedDict(
    "_RequiredIndexConfigurationSummaryTypeDef",
    {
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "Status": Literal[
            "CREATING", "ACTIVE", "DELETING", "FAILED", "UPDATING", "SYSTEM_UPDATING"
        ],
    },
)
_OptionalIndexConfigurationSummaryTypeDef = TypedDict(
    "_OptionalIndexConfigurationSummaryTypeDef",
    {"Name": str, "Id": str, "Edition": Literal["DEVELOPER_EDITION", "ENTERPRISE_EDITION"]},
    total=False,
)


class IndexConfigurationSummaryTypeDef(
    _RequiredIndexConfigurationSummaryTypeDef, _OptionalIndexConfigurationSummaryTypeDef
):
    pass


ListIndicesResponseTypeDef = TypedDict(
    "ListIndicesResponseTypeDef",
    {"IndexConfigurationSummaryItems": List[IndexConfigurationSummaryTypeDef], "NextToken": str},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef]}, total=False
)

DocumentAttributeValueCountPairTypeDef = TypedDict(
    "DocumentAttributeValueCountPairTypeDef",
    {"DocumentAttributeValue": DocumentAttributeValueTypeDef, "Count": int},
    total=False,
)

FacetResultTypeDef = TypedDict(
    "FacetResultTypeDef",
    {
        "DocumentAttributeKey": str,
        "DocumentAttributeValueCountPairs": List[DocumentAttributeValueCountPairTypeDef],
    },
    total=False,
)

_RequiredHighlightTypeDef = TypedDict(
    "_RequiredHighlightTypeDef", {"BeginOffset": int, "EndOffset": int}
)
_OptionalHighlightTypeDef = TypedDict("_OptionalHighlightTypeDef", {"TopAnswer": bool}, total=False)


class HighlightTypeDef(_RequiredHighlightTypeDef, _OptionalHighlightTypeDef):
    pass


TextWithHighlightsTypeDef = TypedDict(
    "TextWithHighlightsTypeDef", {"Text": str, "Highlights": List[HighlightTypeDef]}, total=False
)

AdditionalResultAttributeValueTypeDef = TypedDict(
    "AdditionalResultAttributeValueTypeDef",
    {"TextWithHighlightsValue": TextWithHighlightsTypeDef},
    total=False,
)

AdditionalResultAttributeTypeDef = TypedDict(
    "AdditionalResultAttributeTypeDef",
    {
        "Key": str,
        "ValueType": Literal["TEXT_WITH_HIGHLIGHTS_VALUE"],
        "Value": AdditionalResultAttributeValueTypeDef,
    },
)

QueryResultItemTypeDef = TypedDict(
    "QueryResultItemTypeDef",
    {
        "Id": str,
        "Type": Literal["DOCUMENT", "QUESTION_ANSWER", "ANSWER"],
        "AdditionalAttributes": List[AdditionalResultAttributeTypeDef],
        "DocumentId": str,
        "DocumentTitle": TextWithHighlightsTypeDef,
        "DocumentExcerpt": TextWithHighlightsTypeDef,
        "DocumentURI": str,
        "DocumentAttributes": List[DocumentAttributeTypeDef],
    },
    total=False,
)

QueryResultTypeDef = TypedDict(
    "QueryResultTypeDef",
    {
        "QueryId": str,
        "ResultItems": List[QueryResultItemTypeDef],
        "FacetResults": List[FacetResultTypeDef],
        "TotalNumberOfResults": int,
    },
    total=False,
)

RelevanceFeedbackTypeDef = TypedDict(
    "RelevanceFeedbackTypeDef",
    {"ResultId": str, "RelevanceValue": Literal["RELEVANT", "NOT_RELEVANT"]},
)

StartDataSourceSyncJobResponseTypeDef = TypedDict(
    "StartDataSourceSyncJobResponseTypeDef", {"ExecutionId": str}, total=False
)

TimeRangeTypeDef = TypedDict(
    "TimeRangeTypeDef", {"StartTime": datetime, "EndTime": datetime}, total=False
)
