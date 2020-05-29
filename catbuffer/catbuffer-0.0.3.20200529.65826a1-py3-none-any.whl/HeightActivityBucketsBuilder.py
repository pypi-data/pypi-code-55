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


class HeightActivityBucketsBuilder:
    """Account activity buckets.

    Attributes:
        buckets: Account activity buckets.
    """

    def __init__(self, buckets: bytes):
        """Constructor.
        Args:
            buckets: Account activity buckets.
        """
        self.buckets = buckets

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> HeightActivityBucketsBuilder:
        """Creates an instance of HeightActivityBucketsBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of HeightActivityBucketsBuilder.
        """
        bytes_ = bytes(payload)
        buckets = GeneratorUtils.getBytes(bytes_, 5)  # kind:BUFFER
        bytes_ = bytes_[5:]
        return HeightActivityBucketsBuilder(buckets)

    def getBuckets(self) -> bytes:
        """Gets account activity buckets.
        Returns:
            Account activity buckets.
        """
        return self.buckets

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += len(self.buckets)
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.buckets)  # kind:BUFFER
        return bytes_
