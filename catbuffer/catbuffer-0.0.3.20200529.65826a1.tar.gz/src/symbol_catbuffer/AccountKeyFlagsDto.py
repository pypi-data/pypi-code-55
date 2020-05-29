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
from enum import Flag
from typing import List
from .GeneratorUtils import GeneratorUtils


class AccountKeyFlagsDto(Flag):
    """Enumeration of account key flags

    Attributes:
        UNSET: unset key.
        LINKED: linked account public key \note this can be either a remote or main account public key depending on context.
        VRF: VRF public key.
        VOTING: voting public key.
        NODE: node public key on which remote is allowed to harvest.
    """

    UNSET = 0
    LINKED = 1
    VRF = 2
    VOTING = 4
    NODE = 8

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountKeyFlagsDto:
        """Creates an instance of AccountKeyFlagsDto from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountKeyFlagsDto.
        """
        value: int = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes(payload), 1))
        return AccountKeyFlagsDto(value)

    @classmethod
    def getSize(cls) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 1

    @classmethod
    def bytesToFlags(cls, bitMaskValue: bytes, size: int) -> List[AccountKeyFlagsDto]:
        """Converts a bit representation to a list of AccountKeyFlagsDto.
        Args:
            bitMaskValue Bitmask bytes value.
        Returns:
            List of AccountKeyFlagsDto flags representing the int value.
        """
        return cls.intToFlags(GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bitMaskValue, size)))

    @classmethod
    def intToFlags(cls, bitMaskValue: int) -> List[AccountKeyFlagsDto]:
        """Converts a bit representation to a list of AccountKeyFlagsDto.
        Args:
            bitMaskValue Bitmask int value.
        Returns:
            List of AccountKeyFlagsDto flags representing the int value.
        """
        results = []
        for flag in AccountKeyFlagsDto:
            if 0 != flag.value & bitMaskValue:
                results.append(flag)
        return results

    @classmethod
    def flagsToInt(cls, flags: List[AccountKeyFlagsDto]) -> int:
        """Converts a list of AccountKeyFlagsDto to a bit representation.
        Args:
            List of AccountKeyFlagsDto flags representing the int value.
        Returns:
            int value of the list of flags
        """
        result = 0
        for flag in AccountKeyFlagsDto:
            if flag in flags:
                result += flag.value
        return result

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.value, 1))
        return bytes_
