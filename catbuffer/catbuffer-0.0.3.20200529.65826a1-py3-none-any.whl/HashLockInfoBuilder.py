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
from .Hash256Dto import Hash256Dto
from .HeightDto import HeightDto
from .KeyDto import KeyDto
from .LockStatusDto import LockStatusDto
from .MosaicBuilder import MosaicBuilder


class HashLockInfoBuilder:
    """Binary layout for hash lock transaction info.

    Attributes:
        senderPublicKey: Sender public key.
        mosaic: Mosaic associated with lock.
        endHeight: Height at which the lock expires.
        status: Flag indicating whether or not the lock was already used.
        hash: Hash.
    """

    def __init__(self, senderPublicKey: KeyDto, mosaic: MosaicBuilder, endHeight: HeightDto, status: LockStatusDto, hash: Hash256Dto):
        """Constructor.
        Args:
            senderPublicKey: Sender public key.
            mosaic: Mosaic associated with lock.
            endHeight: Height at which the lock expires.
            status: Flag indicating whether or not the lock was already used.
            hash: Hash.
        """
        self.senderPublicKey = senderPublicKey
        self.mosaic = mosaic
        self.endHeight = endHeight
        self.status = status
        self.hash = hash

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> HashLockInfoBuilder:
        """Creates an instance of HashLockInfoBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of HashLockInfoBuilder.
        """
        bytes_ = bytes(payload)
        senderPublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[senderPublicKey.getSize():]
        mosaic = MosaicBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[mosaic.getSize():]
        endHeight = HeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[endHeight.getSize():]
        status = LockStatusDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[status.getSize():]
        hash = Hash256Dto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[hash.getSize():]
        return HashLockInfoBuilder(senderPublicKey, mosaic, endHeight, status, hash)

    def getSenderPublicKey(self) -> KeyDto:
        """Gets sender public key.
        Returns:
            Sender public key.
        """
        return self.senderPublicKey

    def getMosaic(self) -> MosaicBuilder:
        """Gets mosaic associated with lock.
        Returns:
            Mosaic associated with lock.
        """
        return self.mosaic

    def getEndHeight(self) -> HeightDto:
        """Gets height at which the lock expires.
        Returns:
            Height at which the lock expires.
        """
        return self.endHeight

    def getStatus(self) -> LockStatusDto:
        """Gets flag indicating whether or not the lock was already used.
        Returns:
            Flag indicating whether or not the lock was already used.
        """
        return self.status

    def getHash(self) -> Hash256Dto:
        """Gets hash.
        Returns:
            Hash.
        """
        return self.hash

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.senderPublicKey.getSize()
        size += self.mosaic.getSize()
        size += self.endHeight.getSize()
        size += self.status.getSize()
        size += self.hash.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.senderPublicKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.mosaic.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.endHeight.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.status.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.hash.serialize())  # kind:CUSTOM
        return bytes_
