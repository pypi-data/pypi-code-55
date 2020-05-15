"""
Main interface for pinpoint-email service type definitions.

Usage::

    from mypy_boto3.pinpoint_email.type_defs import CreateDeliverabilityTestReportResponseTypeDef

    data: CreateDeliverabilityTestReportResponseTypeDef = {...}
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
    "CreateDeliverabilityTestReportResponseTypeDef",
    "DkimAttributesTypeDef",
    "CreateEmailIdentityResponseTypeDef",
    "DeliveryOptionsTypeDef",
    "DestinationTypeDef",
    "InboxPlacementTrackingOptionTypeDef",
    "DomainDeliverabilityTrackingOptionTypeDef",
    "ContentTypeDef",
    "BodyTypeDef",
    "MessageTypeDef",
    "RawMessageTypeDef",
    "TemplateTypeDef",
    "EmailContentTypeDef",
    "CloudWatchDimensionConfigurationTypeDef",
    "CloudWatchDestinationTypeDef",
    "KinesisFirehoseDestinationTypeDef",
    "PinpointDestinationTypeDef",
    "SnsDestinationTypeDef",
    "EventDestinationDefinitionTypeDef",
    "SendQuotaTypeDef",
    "GetAccountResponseTypeDef",
    "BlacklistEntryTypeDef",
    "GetBlacklistReportsResponseTypeDef",
    "EventDestinationTypeDef",
    "GetConfigurationSetEventDestinationsResponseTypeDef",
    "ReputationOptionsTypeDef",
    "SendingOptionsTypeDef",
    "TagTypeDef",
    "TrackingOptionsTypeDef",
    "GetConfigurationSetResponseTypeDef",
    "DedicatedIpTypeDef",
    "GetDedicatedIpResponseTypeDef",
    "GetDedicatedIpsResponseTypeDef",
    "GetDeliverabilityDashboardOptionsResponseTypeDef",
    "DeliverabilityTestReportTypeDef",
    "PlacementStatisticsTypeDef",
    "IspPlacementTypeDef",
    "GetDeliverabilityTestReportResponseTypeDef",
    "DomainDeliverabilityCampaignTypeDef",
    "GetDomainDeliverabilityCampaignResponseTypeDef",
    "DomainIspPlacementTypeDef",
    "VolumeStatisticsTypeDef",
    "DailyVolumeTypeDef",
    "OverallVolumeTypeDef",
    "GetDomainStatisticsReportResponseTypeDef",
    "MailFromAttributesTypeDef",
    "GetEmailIdentityResponseTypeDef",
    "ListConfigurationSetsResponseTypeDef",
    "ListDedicatedIpPoolsResponseTypeDef",
    "ListDeliverabilityTestReportsResponseTypeDef",
    "ListDomainDeliverabilityCampaignsResponseTypeDef",
    "IdentityInfoTypeDef",
    "ListEmailIdentitiesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MessageTagTypeDef",
    "PaginatorConfigTypeDef",
    "SendEmailResponseTypeDef",
)

CreateDeliverabilityTestReportResponseTypeDef = TypedDict(
    "CreateDeliverabilityTestReportResponseTypeDef",
    {"ReportId": str, "DeliverabilityTestStatus": Literal["IN_PROGRESS", "COMPLETED"]},
)

DkimAttributesTypeDef = TypedDict(
    "DkimAttributesTypeDef",
    {
        "SigningEnabled": bool,
        "Status": Literal["PENDING", "SUCCESS", "FAILED", "TEMPORARY_FAILURE", "NOT_STARTED"],
        "Tokens": List[str],
    },
    total=False,
)

CreateEmailIdentityResponseTypeDef = TypedDict(
    "CreateEmailIdentityResponseTypeDef",
    {
        "IdentityType": Literal["EMAIL_ADDRESS", "DOMAIN", "MANAGED_DOMAIN"],
        "VerifiedForSendingStatus": bool,
        "DkimAttributes": DkimAttributesTypeDef,
    },
    total=False,
)

DeliveryOptionsTypeDef = TypedDict(
    "DeliveryOptionsTypeDef",
    {"TlsPolicy": Literal["REQUIRE", "OPTIONAL"], "SendingPoolName": str},
    total=False,
)

DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {"ToAddresses": List[str], "CcAddresses": List[str], "BccAddresses": List[str]},
    total=False,
)

InboxPlacementTrackingOptionTypeDef = TypedDict(
    "InboxPlacementTrackingOptionTypeDef", {"Global": bool, "TrackedIsps": List[str]}, total=False
)

DomainDeliverabilityTrackingOptionTypeDef = TypedDict(
    "DomainDeliverabilityTrackingOptionTypeDef",
    {
        "Domain": str,
        "SubscriptionStartDate": datetime,
        "InboxPlacementTrackingOption": InboxPlacementTrackingOptionTypeDef,
    },
    total=False,
)

_RequiredContentTypeDef = TypedDict("_RequiredContentTypeDef", {"Data": str})
_OptionalContentTypeDef = TypedDict("_OptionalContentTypeDef", {"Charset": str}, total=False)


class ContentTypeDef(_RequiredContentTypeDef, _OptionalContentTypeDef):
    pass


BodyTypeDef = TypedDict(
    "BodyTypeDef", {"Text": ContentTypeDef, "Html": ContentTypeDef}, total=False
)

MessageTypeDef = TypedDict("MessageTypeDef", {"Subject": ContentTypeDef, "Body": BodyTypeDef})

RawMessageTypeDef = TypedDict("RawMessageTypeDef", {"Data": Union[bytes, IO]})

TemplateTypeDef = TypedDict(
    "TemplateTypeDef", {"TemplateArn": str, "TemplateData": str}, total=False
)

EmailContentTypeDef = TypedDict(
    "EmailContentTypeDef",
    {"Simple": MessageTypeDef, "Raw": RawMessageTypeDef, "Template": TemplateTypeDef},
    total=False,
)

CloudWatchDimensionConfigurationTypeDef = TypedDict(
    "CloudWatchDimensionConfigurationTypeDef",
    {
        "DimensionName": str,
        "DimensionValueSource": Literal["MESSAGE_TAG", "EMAIL_HEADER", "LINK_TAG"],
        "DefaultDimensionValue": str,
    },
)

CloudWatchDestinationTypeDef = TypedDict(
    "CloudWatchDestinationTypeDef",
    {"DimensionConfigurations": List[CloudWatchDimensionConfigurationTypeDef]},
)

KinesisFirehoseDestinationTypeDef = TypedDict(
    "KinesisFirehoseDestinationTypeDef", {"IamRoleArn": str, "DeliveryStreamArn": str}
)

PinpointDestinationTypeDef = TypedDict(
    "PinpointDestinationTypeDef", {"ApplicationArn": str}, total=False
)

SnsDestinationTypeDef = TypedDict("SnsDestinationTypeDef", {"TopicArn": str})

EventDestinationDefinitionTypeDef = TypedDict(
    "EventDestinationDefinitionTypeDef",
    {
        "Enabled": bool,
        "MatchingEventTypes": List[
            Literal[
                "SEND",
                "REJECT",
                "BOUNCE",
                "COMPLAINT",
                "DELIVERY",
                "OPEN",
                "CLICK",
                "RENDERING_FAILURE",
            ]
        ],
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "CloudWatchDestination": CloudWatchDestinationTypeDef,
        "SnsDestination": SnsDestinationTypeDef,
        "PinpointDestination": PinpointDestinationTypeDef,
    },
    total=False,
)

SendQuotaTypeDef = TypedDict(
    "SendQuotaTypeDef",
    {"Max24HourSend": float, "MaxSendRate": float, "SentLast24Hours": float},
    total=False,
)

GetAccountResponseTypeDef = TypedDict(
    "GetAccountResponseTypeDef",
    {
        "SendQuota": SendQuotaTypeDef,
        "SendingEnabled": bool,
        "DedicatedIpAutoWarmupEnabled": bool,
        "EnforcementStatus": str,
        "ProductionAccessEnabled": bool,
    },
    total=False,
)

BlacklistEntryTypeDef = TypedDict(
    "BlacklistEntryTypeDef",
    {"RblName": str, "ListingTime": datetime, "Description": str},
    total=False,
)

GetBlacklistReportsResponseTypeDef = TypedDict(
    "GetBlacklistReportsResponseTypeDef",
    {"BlacklistReport": Dict[str, List[BlacklistEntryTypeDef]]},
)

_RequiredEventDestinationTypeDef = TypedDict(
    "_RequiredEventDestinationTypeDef",
    {
        "Name": str,
        "MatchingEventTypes": List[
            Literal[
                "SEND",
                "REJECT",
                "BOUNCE",
                "COMPLAINT",
                "DELIVERY",
                "OPEN",
                "CLICK",
                "RENDERING_FAILURE",
            ]
        ],
    },
)
_OptionalEventDestinationTypeDef = TypedDict(
    "_OptionalEventDestinationTypeDef",
    {
        "Enabled": bool,
        "KinesisFirehoseDestination": KinesisFirehoseDestinationTypeDef,
        "CloudWatchDestination": CloudWatchDestinationTypeDef,
        "SnsDestination": SnsDestinationTypeDef,
        "PinpointDestination": PinpointDestinationTypeDef,
    },
    total=False,
)


class EventDestinationTypeDef(_RequiredEventDestinationTypeDef, _OptionalEventDestinationTypeDef):
    pass


GetConfigurationSetEventDestinationsResponseTypeDef = TypedDict(
    "GetConfigurationSetEventDestinationsResponseTypeDef",
    {"EventDestinations": List[EventDestinationTypeDef]},
    total=False,
)

ReputationOptionsTypeDef = TypedDict(
    "ReputationOptionsTypeDef",
    {"ReputationMetricsEnabled": bool, "LastFreshStart": datetime},
    total=False,
)

SendingOptionsTypeDef = TypedDict("SendingOptionsTypeDef", {"SendingEnabled": bool}, total=False)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

TrackingOptionsTypeDef = TypedDict("TrackingOptionsTypeDef", {"CustomRedirectDomain": str})

GetConfigurationSetResponseTypeDef = TypedDict(
    "GetConfigurationSetResponseTypeDef",
    {
        "ConfigurationSetName": str,
        "TrackingOptions": TrackingOptionsTypeDef,
        "DeliveryOptions": DeliveryOptionsTypeDef,
        "ReputationOptions": ReputationOptionsTypeDef,
        "SendingOptions": SendingOptionsTypeDef,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

_RequiredDedicatedIpTypeDef = TypedDict(
    "_RequiredDedicatedIpTypeDef",
    {"Ip": str, "WarmupStatus": Literal["IN_PROGRESS", "DONE"], "WarmupPercentage": int},
)
_OptionalDedicatedIpTypeDef = TypedDict(
    "_OptionalDedicatedIpTypeDef", {"PoolName": str}, total=False
)


class DedicatedIpTypeDef(_RequiredDedicatedIpTypeDef, _OptionalDedicatedIpTypeDef):
    pass


GetDedicatedIpResponseTypeDef = TypedDict(
    "GetDedicatedIpResponseTypeDef", {"DedicatedIp": DedicatedIpTypeDef}, total=False
)

GetDedicatedIpsResponseTypeDef = TypedDict(
    "GetDedicatedIpsResponseTypeDef",
    {"DedicatedIps": List[DedicatedIpTypeDef], "NextToken": str},
    total=False,
)

_RequiredGetDeliverabilityDashboardOptionsResponseTypeDef = TypedDict(
    "_RequiredGetDeliverabilityDashboardOptionsResponseTypeDef", {"DashboardEnabled": bool}
)
_OptionalGetDeliverabilityDashboardOptionsResponseTypeDef = TypedDict(
    "_OptionalGetDeliverabilityDashboardOptionsResponseTypeDef",
    {
        "SubscriptionExpiryDate": datetime,
        "AccountStatus": Literal["ACTIVE", "PENDING_EXPIRATION", "DISABLED"],
        "ActiveSubscribedDomains": List[DomainDeliverabilityTrackingOptionTypeDef],
        "PendingExpirationSubscribedDomains": List[DomainDeliverabilityTrackingOptionTypeDef],
    },
    total=False,
)


class GetDeliverabilityDashboardOptionsResponseTypeDef(
    _RequiredGetDeliverabilityDashboardOptionsResponseTypeDef,
    _OptionalGetDeliverabilityDashboardOptionsResponseTypeDef,
):
    pass


DeliverabilityTestReportTypeDef = TypedDict(
    "DeliverabilityTestReportTypeDef",
    {
        "ReportId": str,
        "ReportName": str,
        "Subject": str,
        "FromEmailAddress": str,
        "CreateDate": datetime,
        "DeliverabilityTestStatus": Literal["IN_PROGRESS", "COMPLETED"],
    },
    total=False,
)

PlacementStatisticsTypeDef = TypedDict(
    "PlacementStatisticsTypeDef",
    {
        "InboxPercentage": float,
        "SpamPercentage": float,
        "MissingPercentage": float,
        "SpfPercentage": float,
        "DkimPercentage": float,
    },
    total=False,
)

IspPlacementTypeDef = TypedDict(
    "IspPlacementTypeDef",
    {"IspName": str, "PlacementStatistics": PlacementStatisticsTypeDef},
    total=False,
)

_RequiredGetDeliverabilityTestReportResponseTypeDef = TypedDict(
    "_RequiredGetDeliverabilityTestReportResponseTypeDef",
    {
        "DeliverabilityTestReport": DeliverabilityTestReportTypeDef,
        "OverallPlacement": PlacementStatisticsTypeDef,
        "IspPlacements": List[IspPlacementTypeDef],
    },
)
_OptionalGetDeliverabilityTestReportResponseTypeDef = TypedDict(
    "_OptionalGetDeliverabilityTestReportResponseTypeDef",
    {"Message": str, "Tags": List[TagTypeDef]},
    total=False,
)


class GetDeliverabilityTestReportResponseTypeDef(
    _RequiredGetDeliverabilityTestReportResponseTypeDef,
    _OptionalGetDeliverabilityTestReportResponseTypeDef,
):
    pass


DomainDeliverabilityCampaignTypeDef = TypedDict(
    "DomainDeliverabilityCampaignTypeDef",
    {
        "CampaignId": str,
        "ImageUrl": str,
        "Subject": str,
        "FromAddress": str,
        "SendingIps": List[str],
        "FirstSeenDateTime": datetime,
        "LastSeenDateTime": datetime,
        "InboxCount": int,
        "SpamCount": int,
        "ReadRate": float,
        "DeleteRate": float,
        "ReadDeleteRate": float,
        "ProjectedVolume": int,
        "Esps": List[str],
    },
    total=False,
)

GetDomainDeliverabilityCampaignResponseTypeDef = TypedDict(
    "GetDomainDeliverabilityCampaignResponseTypeDef",
    {"DomainDeliverabilityCampaign": DomainDeliverabilityCampaignTypeDef},
)

DomainIspPlacementTypeDef = TypedDict(
    "DomainIspPlacementTypeDef",
    {
        "IspName": str,
        "InboxRawCount": int,
        "SpamRawCount": int,
        "InboxPercentage": float,
        "SpamPercentage": float,
    },
    total=False,
)

VolumeStatisticsTypeDef = TypedDict(
    "VolumeStatisticsTypeDef",
    {"InboxRawCount": int, "SpamRawCount": int, "ProjectedInbox": int, "ProjectedSpam": int},
    total=False,
)

DailyVolumeTypeDef = TypedDict(
    "DailyVolumeTypeDef",
    {
        "StartDate": datetime,
        "VolumeStatistics": VolumeStatisticsTypeDef,
        "DomainIspPlacements": List[DomainIspPlacementTypeDef],
    },
    total=False,
)

OverallVolumeTypeDef = TypedDict(
    "OverallVolumeTypeDef",
    {
        "VolumeStatistics": VolumeStatisticsTypeDef,
        "ReadRatePercent": float,
        "DomainIspPlacements": List[DomainIspPlacementTypeDef],
    },
    total=False,
)

GetDomainStatisticsReportResponseTypeDef = TypedDict(
    "GetDomainStatisticsReportResponseTypeDef",
    {"OverallVolume": OverallVolumeTypeDef, "DailyVolumes": List[DailyVolumeTypeDef]},
)

MailFromAttributesTypeDef = TypedDict(
    "MailFromAttributesTypeDef",
    {
        "MailFromDomain": str,
        "MailFromDomainStatus": Literal["PENDING", "SUCCESS", "FAILED", "TEMPORARY_FAILURE"],
        "BehaviorOnMxFailure": Literal["USE_DEFAULT_VALUE", "REJECT_MESSAGE"],
    },
)

GetEmailIdentityResponseTypeDef = TypedDict(
    "GetEmailIdentityResponseTypeDef",
    {
        "IdentityType": Literal["EMAIL_ADDRESS", "DOMAIN", "MANAGED_DOMAIN"],
        "FeedbackForwardingStatus": bool,
        "VerifiedForSendingStatus": bool,
        "DkimAttributes": DkimAttributesTypeDef,
        "MailFromAttributes": MailFromAttributesTypeDef,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

ListConfigurationSetsResponseTypeDef = TypedDict(
    "ListConfigurationSetsResponseTypeDef",
    {"ConfigurationSets": List[str], "NextToken": str},
    total=False,
)

ListDedicatedIpPoolsResponseTypeDef = TypedDict(
    "ListDedicatedIpPoolsResponseTypeDef",
    {"DedicatedIpPools": List[str], "NextToken": str},
    total=False,
)

_RequiredListDeliverabilityTestReportsResponseTypeDef = TypedDict(
    "_RequiredListDeliverabilityTestReportsResponseTypeDef",
    {"DeliverabilityTestReports": List[DeliverabilityTestReportTypeDef]},
)
_OptionalListDeliverabilityTestReportsResponseTypeDef = TypedDict(
    "_OptionalListDeliverabilityTestReportsResponseTypeDef", {"NextToken": str}, total=False
)


class ListDeliverabilityTestReportsResponseTypeDef(
    _RequiredListDeliverabilityTestReportsResponseTypeDef,
    _OptionalListDeliverabilityTestReportsResponseTypeDef,
):
    pass


_RequiredListDomainDeliverabilityCampaignsResponseTypeDef = TypedDict(
    "_RequiredListDomainDeliverabilityCampaignsResponseTypeDef",
    {"DomainDeliverabilityCampaigns": List[DomainDeliverabilityCampaignTypeDef]},
)
_OptionalListDomainDeliverabilityCampaignsResponseTypeDef = TypedDict(
    "_OptionalListDomainDeliverabilityCampaignsResponseTypeDef", {"NextToken": str}, total=False
)


class ListDomainDeliverabilityCampaignsResponseTypeDef(
    _RequiredListDomainDeliverabilityCampaignsResponseTypeDef,
    _OptionalListDomainDeliverabilityCampaignsResponseTypeDef,
):
    pass


IdentityInfoTypeDef = TypedDict(
    "IdentityInfoTypeDef",
    {
        "IdentityType": Literal["EMAIL_ADDRESS", "DOMAIN", "MANAGED_DOMAIN"],
        "IdentityName": str,
        "SendingEnabled": bool,
    },
    total=False,
)

ListEmailIdentitiesResponseTypeDef = TypedDict(
    "ListEmailIdentitiesResponseTypeDef",
    {"EmailIdentities": List[IdentityInfoTypeDef], "NextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List[TagTypeDef]}
)

MessageTagTypeDef = TypedDict("MessageTagTypeDef", {"Name": str, "Value": str})

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

SendEmailResponseTypeDef = TypedDict("SendEmailResponseTypeDef", {"MessageId": str}, total=False)
