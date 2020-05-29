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
from .KeyDto import KeyDto
from .MetadataTypeDto import MetadataTypeDto
from .MetadataValueBuilder import MetadataValueBuilder
from .ScopedMetadataKeyDto import ScopedMetadataKeyDto


class MetadataEntryBuilder:
    """Binary layout of a metadata entry.

    Attributes:
        sourcePublicKey: Metadata source public key (provider).
        targetPublicKey: Public key of the metadata target.
        scopedMetadataKey: Metadata key scoped to source, target and type.
        targetId: Target id.
        metadataType: Metadata type.
        value: Value.
    """

    def __init__(self, sourcePublicKey: KeyDto, targetPublicKey: KeyDto, scopedMetadataKey: ScopedMetadataKeyDto, targetId: int, metadataType: MetadataTypeDto, value: MetadataValueBuilder):
        """Constructor.
        Args:
            sourcePublicKey: Metadata source public key (provider).
            targetPublicKey: Public key of the metadata target.
            scopedMetadataKey: Metadata key scoped to source, target and type.
            targetId: Target id.
            metadataType: Metadata type.
            value: Value.
        """
        self.sourcePublicKey = sourcePublicKey
        self.targetPublicKey = targetPublicKey
        self.scopedMetadataKey = scopedMetadataKey
        self.targetId = targetId
        self.metadataType = metadataType
        self.value = value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MetadataEntryBuilder:
        """Creates an instance of MetadataEntryBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MetadataEntryBuilder.
        """
        bytes_ = bytes(payload)
        sourcePublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[sourcePublicKey.getSize():]
        targetPublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[targetPublicKey.getSize():]
        scopedMetadataKey = ScopedMetadataKeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[scopedMetadataKey.getSize():]
        targetId = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        metadataType = MetadataTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[metadataType.getSize():]
        value = MetadataValueBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[value.getSize():]
        return MetadataEntryBuilder(sourcePublicKey, targetPublicKey, scopedMetadataKey, targetId, metadataType, value)

    def getSourcePublicKey(self) -> KeyDto:
        """Gets metadata source public key (provider).
        Returns:
            Metadata source public key (provider).
        """
        return self.sourcePublicKey

    def getTargetPublicKey(self) -> KeyDto:
        """Gets public key of the metadata target.
        Returns:
            Public key of the metadata target.
        """
        return self.targetPublicKey

    def getScopedMetadataKey(self) -> ScopedMetadataKeyDto:
        """Gets metadata key scoped to source, target and type.
        Returns:
            Metadata key scoped to source, target and type.
        """
        return self.scopedMetadataKey

    def getTargetId(self) -> int:
        """Gets target id.
        Returns:
            Target id.
        """
        return self.targetId

    def getMetadataType(self) -> MetadataTypeDto:
        """Gets metadata type.
        Returns:
            Metadata type.
        """
        return self.metadataType

    def getValue(self) -> MetadataValueBuilder:
        """Gets value.
        Returns:
            Value.
        """
        return self.value

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.sourcePublicKey.getSize()
        size += self.targetPublicKey.getSize()
        size += self.scopedMetadataKey.getSize()
        size += 8  # targetId
        size += self.metadataType.getSize()
        size += self.value.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.sourcePublicKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.targetPublicKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.scopedMetadataKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getTargetId(), 8))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.metadataType.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.value.serialize())  # kind:CUSTOM
        return bytes_
