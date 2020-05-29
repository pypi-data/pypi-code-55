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


class MetadataValueBuilder:
    """Binary layout of a metadata entry value.

    Attributes:
        size: Size of the value.
        data: Data of the value.
    """

    def __init__(self, size: int, data: bytes):
        """Constructor.
        Args:
            size: Size of the value.
            data: Data of the value.
        """
        self.size = size
        self.data = data

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MetadataValueBuilder:
        """Creates an instance of MetadataValueBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MetadataValueBuilder.
        """
        bytes_ = bytes(payload)
        size = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))  # kind:SIMPLE
        bytes_ = bytes_[2:]
        data = GeneratorUtils.getBytes(bytes_, size)  # kind:BUFFER
        bytes_ = bytes_[size:]
        return MetadataValueBuilder(size, data)

    def getBytesSize(self) -> int:
        """Gets size of the value.
        Returns:
            Size of the value.
        """
        return self.size

    def getData(self) -> bytes:
        """Gets data of the value.
        Returns:
            Data of the value.
        """
        return self.data

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 2  # size
        size += len(self.data)
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getSize(), 2))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.data)  # kind:BUFFER
        return bytes_
