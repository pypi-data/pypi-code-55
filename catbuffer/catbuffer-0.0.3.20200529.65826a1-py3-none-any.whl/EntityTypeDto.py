#!/usr/bin/python
"""
    Copyright (c) 2016-present,
    Jaguar0625, gimre, BloodyRookie, Tech Bureau, Corp. All rights reserved.

    This file is part of Catapult.

    Catapult is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Catapult is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Catapult. If not, see <http://www.gnu.org/licenses/>.
"""

# pylint: disable=W0622,W0612,C0301,R0904

from __future__ import annotations
from enum import Enum
from .GeneratorUtils import GeneratorUtils


class EntityTypeDto(Enum):
    """Enumeration of entity types

    Attributes:
        RESERVED: reserved entity type.
        MOSAIC_DEFINITION_TRANSACTION_BUILDER: Mosaic definition transaction builder.
        ACCOUNT_KEY_LINK_TRANSACTION_BUILDER: Account key link transaction builder.
        NODE_KEY_LINK_TRANSACTION_BUILDER: Node key link transaction builder.
        AGGREGATE_COMPLETE_TRANSACTION_BUILDER: Aggregate complete transaction builder.
        AGGREGATE_BONDED_TRANSACTION_BUILDER: Aggregate bonded transaction builder.
        VOTING_KEY_LINK_TRANSACTION_BUILDER: Voting key link transaction builder.
        VRF_KEY_LINK_TRANSACTION_BUILDER: Vrf key link transaction builder.
        HASH_LOCK_TRANSACTION_BUILDER: Hash lock transaction builder.
        SECRET_LOCK_TRANSACTION_BUILDER: Secret lock transaction builder.
        SECRET_PROOF_TRANSACTION_BUILDER: Secret proof transaction builder.
        ACCOUNT_METADATA_TRANSACTION_BUILDER: Account metadata transaction builder.
        MOSAIC_METADATA_TRANSACTION_BUILDER: Mosaic metadata transaction builder.
        NAMESPACE_METADATA_TRANSACTION_BUILDER: Namespace metadata transaction builder.
        MOSAIC_SUPPLY_CHANGE_TRANSACTION_BUILDER: Mosaic supply change transaction builder.
        MULTISIG_ACCOUNT_MODIFICATION_TRANSACTION_BUILDER: Multisig account modification transaction builder.
        ADDRESS_ALIAS_TRANSACTION_BUILDER: Address alias transaction builder.
        MOSAIC_ALIAS_TRANSACTION_BUILDER: Mosaic alias transaction builder.
        NAMESPACE_REGISTRATION_TRANSACTION_BUILDER: Namespace registration transaction builder.
        ACCOUNT_ADDRESS_RESTRICTION_TRANSACTION_BUILDER: Account address restriction transaction builder.
        ACCOUNT_MOSAIC_RESTRICTION_TRANSACTION_BUILDER: Account mosaic restriction transaction builder.
        ACCOUNT_OPERATION_RESTRICTION_TRANSACTION_BUILDER: Account operation restriction transaction builder.
        MOSAIC_ADDRESS_RESTRICTION_TRANSACTION_BUILDER: Mosaic address restriction transaction builder.
        MOSAIC_GLOBAL_RESTRICTION_TRANSACTION_BUILDER: Mosaic global restriction transaction builder.
        TRANSFER_TRANSACTION_BUILDER: Transfer transaction builder.
    """

    RESERVED = 0
    MOSAIC_DEFINITION_TRANSACTION_BUILDER = 16717
    ACCOUNT_KEY_LINK_TRANSACTION_BUILDER = 16716
    NODE_KEY_LINK_TRANSACTION_BUILDER = 16972
    AGGREGATE_COMPLETE_TRANSACTION_BUILDER = 16705
    AGGREGATE_BONDED_TRANSACTION_BUILDER = 16961
    VOTING_KEY_LINK_TRANSACTION_BUILDER = 16707
    VRF_KEY_LINK_TRANSACTION_BUILDER = 16963
    HASH_LOCK_TRANSACTION_BUILDER = 16712
    SECRET_LOCK_TRANSACTION_BUILDER = 16722
    SECRET_PROOF_TRANSACTION_BUILDER = 16978
    ACCOUNT_METADATA_TRANSACTION_BUILDER = 16708
    MOSAIC_METADATA_TRANSACTION_BUILDER = 16964
    NAMESPACE_METADATA_TRANSACTION_BUILDER = 17220
    MOSAIC_SUPPLY_CHANGE_TRANSACTION_BUILDER = 16973
    MULTISIG_ACCOUNT_MODIFICATION_TRANSACTION_BUILDER = 16725
    ADDRESS_ALIAS_TRANSACTION_BUILDER = 16974
    MOSAIC_ALIAS_TRANSACTION_BUILDER = 17230
    NAMESPACE_REGISTRATION_TRANSACTION_BUILDER = 16718
    ACCOUNT_ADDRESS_RESTRICTION_TRANSACTION_BUILDER = 16720
    ACCOUNT_MOSAIC_RESTRICTION_TRANSACTION_BUILDER = 16976
    ACCOUNT_OPERATION_RESTRICTION_TRANSACTION_BUILDER = 17232
    MOSAIC_ADDRESS_RESTRICTION_TRANSACTION_BUILDER = 16977
    MOSAIC_GLOBAL_RESTRICTION_TRANSACTION_BUILDER = 16721
    TRANSFER_TRANSACTION_BUILDER = 16724

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EntityTypeDto:
        """Creates an instance of EntityTypeDto from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EntityTypeDto.
        """
        value: int = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes(payload), 2))
        return EntityTypeDto(value)

    @classmethod
    def getSize(cls) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 2

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.value, 2))
        return bytes_
