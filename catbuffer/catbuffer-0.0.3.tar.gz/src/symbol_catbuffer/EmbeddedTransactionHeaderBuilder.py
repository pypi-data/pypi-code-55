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


class EmbeddedTransactionHeaderBuilder:
    """Binary layout for an embedded transaction header.

    Attributes:
        size: Entity size.
        embeddedTransactionHeader_Reserved1: Reserved padding to align end of EmbeddedTransactionHeader on 8-byte boundary.
    """

    def __init__(self, size: int):
        """Constructor.
        Args:
            size: Entity size.
        """
        self.size = size
        self.embeddedTransactionHeader_Reserved1 = 0

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedTransactionHeaderBuilder:
        """Creates an instance of EmbeddedTransactionHeaderBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedTransactionHeaderBuilder.
        """
        bytes_ = bytes(payload)
        size = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        embeddedTransactionHeader_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        return EmbeddedTransactionHeaderBuilder(size)

    def getBytesSize(self) -> int:
        """Gets entity size.
        Returns:
            Entity size.
        """
        return self.size

    def getEmbeddedTransactionHeader_Reserved1(self) -> int:
        """Gets reserved padding to align end of EmbeddedTransactionHeader on 8-byte boundary.
        Returns:
            Reserved padding to align end of EmbeddedTransactionHeader on 8-byte boundary.
        """
        return self.embeddedTransactionHeader_Reserved1

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 4  # size
        size += 4  # embeddedTransactionHeader_Reserved1
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getSize(), 4))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getEmbeddedTransactionHeader_Reserved1(), 4))  # kind:SIMPLE
        return bytes_
