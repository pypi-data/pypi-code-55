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


class MultisigEntryBuilder:
    """Binary layout for a multisig entry.

    Attributes:
        minApproval: Minimum approval for modifications.
        minRemoval: Minimum approval for removal.
        accountPublicKey: Account public key.
        cosignatoryPublicKeys: Cosignatories for account.
        multisigPublicKeys: Accounts for which the entry is cosignatory.
    """

    def __init__(self, minApproval: int, minRemoval: int, accountPublicKey: KeyDto, cosignatoryPublicKeys: List[KeyDto], multisigPublicKeys: List[KeyDto]):
        """Constructor.
        Args:
            minApproval: Minimum approval for modifications.
            minRemoval: Minimum approval for removal.
            accountPublicKey: Account public key.
            cosignatoryPublicKeys: Cosignatories for account.
            multisigPublicKeys: Accounts for which the entry is cosignatory.
        """
        self.minApproval = minApproval
        self.minRemoval = minRemoval
        self.accountPublicKey = accountPublicKey
        self.cosignatoryPublicKeys = cosignatoryPublicKeys
        self.multisigPublicKeys = multisigPublicKeys

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MultisigEntryBuilder:
        """Creates an instance of MultisigEntryBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MultisigEntryBuilder.
        """
        bytes_ = bytes(payload)
        minApproval = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        minRemoval = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        accountPublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[accountPublicKey.getSize():]
        cosignatoryPublicKeysCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIZE_FIELD
        bytes_ = bytes_[8:]
        cosignatoryPublicKeys: List[KeyDto] = []  # kind:ARRAY
        for _ in range(cosignatoryPublicKeysCount):
            item = KeyDto.loadFromBinary(bytes_)
            cosignatoryPublicKeys.append(item)
            bytes_ = bytes_[item.getSize():]
        multisigPublicKeysCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIZE_FIELD
        bytes_ = bytes_[8:]
        multisigPublicKeys: List[KeyDto] = []  # kind:ARRAY
        for _ in range(multisigPublicKeysCount):
            item = KeyDto.loadFromBinary(bytes_)
            multisigPublicKeys.append(item)
            bytes_ = bytes_[item.getSize():]
        return MultisigEntryBuilder(minApproval, minRemoval, accountPublicKey, cosignatoryPublicKeys, multisigPublicKeys)

    def getMinApproval(self) -> int:
        """Gets minimum approval for modifications.
        Returns:
            Minimum approval for modifications.
        """
        return self.minApproval

    def getMinRemoval(self) -> int:
        """Gets minimum approval for removal.
        Returns:
            Minimum approval for removal.
        """
        return self.minRemoval

    def getAccountPublicKey(self) -> KeyDto:
        """Gets account public key.
        Returns:
            Account public key.
        """
        return self.accountPublicKey

    def getCosignatoryPublicKeys(self) -> List[KeyDto]:
        """Gets cosignatories for account.
        Returns:
            Cosignatories for account.
        """
        return self.cosignatoryPublicKeys

    def getMultisigPublicKeys(self) -> List[KeyDto]:
        """Gets accounts for which the entry is cosignatory.
        Returns:
            Accounts for which the entry is cosignatory.
        """
        return self.multisigPublicKeys

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 4  # minApproval
        size += 4  # minRemoval
        size += self.accountPublicKey.getSize()
        size += 8  # cosignatoryPublicKeysCount
        for _ in self.cosignatoryPublicKeys:
            size += _.getSize()
        size += 8  # multisigPublicKeysCount
        for _ in self.multisigPublicKeys:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getMinApproval(), 4))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getMinRemoval(), 4))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.accountPublicKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getCosignatoryPublicKeys()), 8))  # kind:SIZE_FIELD
        for _ in self.cosignatoryPublicKeys:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())  # kind:ARRAY|VAR_ARRAY|FILL_ARRAY
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getMultisigPublicKeys()), 8))  # kind:SIZE_FIELD
        for _ in self.multisigPublicKeys:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())  # kind:ARRAY|VAR_ARRAY|FILL_ARRAY
        return bytes_
