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
from typing import List
from .GeneratorUtils import GeneratorUtils
from .KeyDto import KeyDto


class MultisigAccountModificationTransactionBodyBuilder:
    """Binary layout for a multisig account modification transaction.

    Attributes:
        minRemovalDelta: Relative change of the minimal number of cosignatories required when removing an account.
        minApprovalDelta: Relative change of the minimal number of cosignatories required when approving a transaction.
        multisigAccountModificationTransactionBody_Reserved1: Reserved padding to align publicKeyAdditions on 8-byte boundary.
        publicKeyAdditions: Cosignatory public key additions.
        publicKeyDeletions: Cosignatory public key deletions.
    """

    def __init__(self, minRemovalDelta: int, minApprovalDelta: int, publicKeyAdditions: List[KeyDto], publicKeyDeletions: List[KeyDto]):
        """Constructor.
        Args:
            minRemovalDelta: Relative change of the minimal number of cosignatories required when removing an account.
            minApprovalDelta: Relative change of the minimal number of cosignatories required when approving a transaction.
            publicKeyAdditions: Cosignatory public key additions.
            publicKeyDeletions: Cosignatory public key deletions.
        """
        self.minRemovalDelta = minRemovalDelta
        self.minApprovalDelta = minApprovalDelta
        self.multisigAccountModificationTransactionBody_Reserved1 = 0
        self.publicKeyAdditions = publicKeyAdditions
        self.publicKeyDeletions = publicKeyDeletions

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MultisigAccountModificationTransactionBodyBuilder:
        """Creates an instance of MultisigAccountModificationTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MultisigAccountModificationTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)
        minRemovalDelta = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIMPLE
        bytes_ = bytes_[1:]
        minApprovalDelta = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIMPLE
        bytes_ = bytes_[1:]
        publicKeyAdditionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        publicKeyDeletionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        multisigAccountModificationTransactionBody_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        publicKeyAdditions: List[KeyDto] = []  # kind:ARRAY
        for _ in range(publicKeyAdditionsCount):
            item = KeyDto.loadFromBinary(bytes_)
            publicKeyAdditions.append(item)
            bytes_ = bytes_[item.getSize():]
        publicKeyDeletions: List[KeyDto] = []  # kind:ARRAY
        for _ in range(publicKeyDeletionsCount):
            item = KeyDto.loadFromBinary(bytes_)
            publicKeyDeletions.append(item)
            bytes_ = bytes_[item.getSize():]
        return MultisigAccountModificationTransactionBodyBuilder(minRemovalDelta, minApprovalDelta, publicKeyAdditions, publicKeyDeletions)

    def getMinRemovalDelta(self) -> int:
        """Gets relative change of the minimal number of cosignatories required when removing an account.
        Returns:
            Relative change of the minimal number of cosignatories required when removing an account.
        """
        return self.minRemovalDelta

    def getMinApprovalDelta(self) -> int:
        """Gets relative change of the minimal number of cosignatories required when approving a transaction.
        Returns:
            Relative change of the minimal number of cosignatories required when approving a transaction.
        """
        return self.minApprovalDelta

    def getMultisigAccountModificationTransactionBody_Reserved1(self) -> int:
        """Gets reserved padding to align publicKeyAdditions on 8-byte boundary.
        Returns:
            Reserved padding to align publicKeyAdditions on 8-byte boundary.
        """
        return self.multisigAccountModificationTransactionBody_Reserved1

    def getPublicKeyAdditions(self) -> List[KeyDto]:
        """Gets cosignatory public key additions.
        Returns:
            Cosignatory public key additions.
        """
        return self.publicKeyAdditions

    def getPublicKeyDeletions(self) -> List[KeyDto]:
        """Gets cosignatory public key deletions.
        Returns:
            Cosignatory public key deletions.
        """
        return self.publicKeyDeletions

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 1  # minRemovalDelta
        size += 1  # minApprovalDelta
        size += 1  # publicKeyAdditionsCount
        size += 1  # publicKeyDeletionsCount
        size += 4  # multisigAccountModificationTransactionBody_Reserved1
        for _ in self.publicKeyAdditions:
            size += _.getSize()
        for _ in self.publicKeyDeletions:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getMinRemovalDelta(), 1))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getMinApprovalDelta(), 1))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getPublicKeyAdditions()), 1))  # kind:SIZE_FIELD
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getPublicKeyDeletions()), 1))  # kind:SIZE_FIELD
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getMultisigAccountModificationTransactionBody_Reserved1(), 4))  # kind:SIMPLE
        for _ in self.publicKeyAdditions:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())  # kind:ARRAY|VAR_ARRAY|FILL_ARRAY
        for _ in self.publicKeyDeletions:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())  # kind:ARRAY|VAR_ARRAY|FILL_ARRAY
        return bytes_
