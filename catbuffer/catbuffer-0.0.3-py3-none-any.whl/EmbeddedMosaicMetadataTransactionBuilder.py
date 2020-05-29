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
from .GeneratorUtils import GeneratorUtils
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .MosaicMetadataTransactionBodyBuilder import MosaicMetadataTransactionBodyBuilder
from .NetworkTypeDto import NetworkTypeDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto


class EmbeddedMosaicMetadataTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded mosaic metadata transaction.

    Attributes:
        mosaicMetadataTransactionBody: Mosaic metadata transaction body.
    """

    def __init__(self, size: int, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, targetPublicKey: KeyDto, scopedMetadataKey: int, targetMosaicId: UnresolvedMosaicIdDto, valueSizeDelta: int, value: bytes):
        """Constructor.
        Args:
            size: Entity size.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            targetPublicKey: Metadata target public key.
            scopedMetadataKey: Metadata key scoped to source, target and type.
            targetMosaicId: Target mosaic identifier.
            valueSizeDelta: Change in value size in bytes.
            value: Difference between existing value and new value \note when there is no existing value, new value is same this value \note when there is an existing value, new value is calculated as xor(previous-value, value).
        """
        super().__init__(size, signerPublicKey, version, network, type)
        self.mosaicMetadataTransactionBody = MosaicMetadataTransactionBodyBuilder(targetPublicKey, scopedMetadataKey, targetMosaicId, valueSizeDelta, value)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedMosaicMetadataTransactionBuilder:
        """Creates an instance of EmbeddedMosaicMetadataTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedMosaicMetadataTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        mosaicMetadataTransactionBody = MosaicMetadataTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[mosaicMetadataTransactionBody.getSize():]
        return EmbeddedMosaicMetadataTransactionBuilder(superObject.size, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, mosaicMetadataTransactionBody.targetPublicKey, mosaicMetadataTransactionBody.scopedMetadataKey, mosaicMetadataTransactionBody.targetMosaicId, mosaicMetadataTransactionBody.valueSizeDelta, mosaicMetadataTransactionBody.value)

    def getTargetPublicKey(self) -> KeyDto:
        """Gets metadata target public key.
        Returns:
            Metadata target public key.
        """
        return self.mosaicMetadataTransactionBody.getTargetPublicKey()

    def getScopedMetadataKey(self) -> int:
        """Gets metadata key scoped to source, target and type.
        Returns:
            Metadata key scoped to source, target and type.
        """
        return self.mosaicMetadataTransactionBody.getScopedMetadataKey()

    def getTargetMosaicId(self) -> UnresolvedMosaicIdDto:
        """Gets target mosaic identifier.
        Returns:
            Target mosaic identifier.
        """
        return self.mosaicMetadataTransactionBody.getTargetMosaicId()

    def getValueSizeDelta(self) -> int:
        """Gets change in value size in bytes.
        Returns:
            Change in value size in bytes.
        """
        return self.mosaicMetadataTransactionBody.getValueSizeDelta()

    def getValue(self) -> bytes:
        """Gets difference between existing value and new value \note when there is no existing value, new value is same this value \note when there is an existing value, new value is calculated as xor(previous-value, value).
        Returns:
            Difference between existing value and new value \note when there is no existing value, new value is same this value \note when there is an existing value, new value is calculated as xor(previous-value, value).
        """
        return self.mosaicMetadataTransactionBody.getValue()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.mosaicMetadataTransactionBody.getSize()
        return size

    def getBody(self) -> MosaicMetadataTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.mosaicMetadataTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.mosaicMetadataTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
