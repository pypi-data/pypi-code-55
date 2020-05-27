"""
Main interface for codestar-connections service type definitions.

Usage::

    from mypy_boto3.codestar_connections.type_defs import TagTypeDef

    data: TagTypeDef = {...}
"""
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
    "TagTypeDef",
    "CreateConnectionOutputTypeDef",
    "ConnectionTypeDef",
    "GetConnectionOutputTypeDef",
    "ListConnectionsOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

_RequiredCreateConnectionOutputTypeDef = TypedDict(
    "_RequiredCreateConnectionOutputTypeDef", {"ConnectionArn": str}
)
_OptionalCreateConnectionOutputTypeDef = TypedDict(
    "_OptionalCreateConnectionOutputTypeDef", {"Tags": List[TagTypeDef]}, total=False
)


class CreateConnectionOutputTypeDef(
    _RequiredCreateConnectionOutputTypeDef, _OptionalCreateConnectionOutputTypeDef
):
    pass


ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "ConnectionName": str,
        "ConnectionArn": str,
        "ProviderType": Literal["Bitbucket"],
        "OwnerAccountId": str,
        "ConnectionStatus": Literal["PENDING", "AVAILABLE", "ERROR"],
    },
    total=False,
)

GetConnectionOutputTypeDef = TypedDict(
    "GetConnectionOutputTypeDef", {"Connection": ConnectionTypeDef}, total=False
)

ListConnectionsOutputTypeDef = TypedDict(
    "ListConnectionsOutputTypeDef",
    {"Connections": List[ConnectionTypeDef], "NextToken": str},
    total=False,
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef", {"Tags": List[TagTypeDef]}, total=False
)
