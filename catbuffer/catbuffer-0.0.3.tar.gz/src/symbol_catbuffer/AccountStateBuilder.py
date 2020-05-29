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
from .AccountKeyFlagsDto import AccountKeyFlagsDto
from .AccountStateFormatDto import AccountStateFormatDto
from .AccountTypeDto import AccountTypeDto
from .AddressDto import AddressDto
from .HeightActivityBucketsBuilder import HeightActivityBucketsBuilder
from .HeightDto import HeightDto
from .ImportanceSnapshotBuilder import ImportanceSnapshotBuilder
from .KeyDto import KeyDto
from .MosaicBuilder import MosaicBuilder
from .MosaicIdDto import MosaicIdDto
from .VotingKeyDto import VotingKeyDto


class AccountStateBuilder:
    """Binary layout for non-historical account state.

    Attributes:
        address: Address of account.
        addressHeight: Height at which address has been obtained.
        publicKey: Public key of account.
        publicKeyHeight: Height at which public key has been obtained.
        accountType: Type of account.
        format: Account format.
        supplementalAccountKeysMask: Mask of supplemental account key flags.
        linkedPublicKey: Linked account public key.
        vrfPublicKey: Vrf public key.
        votingPublicKey: Voting public key.
        nodePublicKey: Node public key.
        importanceSnapshots: Current importance snapshot of the account.
        activityBuckets: Activity buckets of the account.
        currencyMosaicId: Currency mosaic id.
        balances: Balances of account.
    """

    def __init__(self, address: AddressDto, addressHeight: HeightDto, publicKey: KeyDto, publicKeyHeight: HeightDto, accountType: AccountTypeDto, format: AccountStateFormatDto, supplementalAccountKeysMask: List[AccountKeyFlagsDto], linkedPublicKey: KeyDto, vrfPublicKey: KeyDto, votingPublicKey: VotingKeyDto, nodePublicKey: KeyDto, importanceSnapshots: ImportanceSnapshotBuilder, activityBuckets: HeightActivityBucketsBuilder, currencyMosaicId: MosaicIdDto, balances: List[MosaicBuilder]):
        """Constructor.
        Args:
            address: Address of account.
            addressHeight: Height at which address has been obtained.
            publicKey: Public key of account.
            publicKeyHeight: Height at which public key has been obtained.
            accountType: Type of account.
            format: Account format.
            supplementalAccountKeysMask: Mask of supplemental account key flags.
            linkedPublicKey: Linked account public key.
            vrfPublicKey: Vrf public key.
            votingPublicKey: Voting public key.
            nodePublicKey: Node public key.
            importanceSnapshots: Current importance snapshot of the account.
            activityBuckets: Activity buckets of the account.
            currencyMosaicId: Currency mosaic id.
            balances: Balances of account.
        """
        self.address = address
        self.addressHeight = addressHeight
        self.publicKey = publicKey
        self.publicKeyHeight = publicKeyHeight
        self.accountType = accountType
        self.format = format
        self.supplementalAccountKeysMask = supplementalAccountKeysMask
        self.linkedPublicKey = linkedPublicKey
        self.vrfPublicKey = vrfPublicKey
        self.votingPublicKey = votingPublicKey
        self.nodePublicKey = nodePublicKey
        self.importanceSnapshots = importanceSnapshots
        self.activityBuckets = activityBuckets
        self.currencyMosaicId = currencyMosaicId
        self.balances = balances

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountStateBuilder:
        """Creates an instance of AccountStateBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountStateBuilder.
        """
        bytes_ = bytes(payload)
        address = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[address.getSize():]
        addressHeight = HeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[addressHeight.getSize():]
        publicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[publicKey.getSize():]
        publicKeyHeight = HeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[publicKeyHeight.getSize():]
        accountType = AccountTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[accountType.getSize():]
        format = AccountStateFormatDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[format.getSize():]
        supplementalAccountKeysMask = AccountKeyFlagsDto.bytesToFlags(bytes_, 1)  # kind:FLAGS
        bytes_ = bytes_[1:]
        currencyMosaicId = MosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[currencyMosaicId.getSize():]
        balancesCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))  # kind:SIZE_FIELD
        bytes_ = bytes_[2:]
        balances: List[MosaicBuilder] = []  # kind:ARRAY
        for _ in range(balancesCount):
            item = MosaicBuilder.loadFromBinary(bytes_)
            balances.append(item)
            bytes_ = bytes_[item.getSize():]
        linkedPublicKey = None
        if AccountKeyFlagsDto.LINKED in supplementalAccountKeysMask:
            linkedPublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM3
        vrfPublicKey = None
        if AccountKeyFlagsDto.VRF in supplementalAccountKeysMask:
            vrfPublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM3
        votingPublicKey = None
        if AccountKeyFlagsDto.VOTING in supplementalAccountKeysMask:
            votingPublicKey = VotingKeyDto.loadFromBinary(bytes_)  # kind:CUSTOM3
        nodePublicKey = None
        if AccountKeyFlagsDto.NODE in supplementalAccountKeysMask:
            nodePublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM3
        importanceSnapshots = None
        if format == AccountStateFormatDto.HIGH_VALUE:
            importanceSnapshots = ImportanceSnapshotBuilder.loadFromBinary(bytes_)  # kind:CUSTOM3
        activityBuckets = None
        if format == AccountStateFormatDto.HIGH_VALUE:
            activityBuckets = HeightActivityBucketsBuilder.loadFromBinary(bytes_)  # kind:CUSTOM3
        return AccountStateBuilder(address, addressHeight, publicKey, publicKeyHeight, accountType, format, supplementalAccountKeysMask, linkedPublicKey, vrfPublicKey, votingPublicKey, nodePublicKey, importanceSnapshots, activityBuckets, currencyMosaicId, balances)

    def getAddress(self) -> AddressDto:
        """Gets address of account.
        Returns:
            Address of account.
        """
        return self.address

    def getAddressHeight(self) -> HeightDto:
        """Gets height at which address has been obtained.
        Returns:
            Height at which address has been obtained.
        """
        return self.addressHeight

    def getPublicKey(self) -> KeyDto:
        """Gets public key of account.
        Returns:
            Public key of account.
        """
        return self.publicKey

    def getPublicKeyHeight(self) -> HeightDto:
        """Gets height at which public key has been obtained.
        Returns:
            Height at which public key has been obtained.
        """
        return self.publicKeyHeight

    def getAccountType(self) -> AccountTypeDto:
        """Gets type of account.
        Returns:
            Type of account.
        """
        return self.accountType

    def getFormat(self) -> AccountStateFormatDto:
        """Gets account format.
        Returns:
            Account format.
        """
        return self.format

    def getSupplementalAccountKeysMask(self) -> List[AccountKeyFlagsDto]:
        """Gets mask of supplemental account key flags.
        Returns:
            Mask of supplemental account key flags.
        """
        return self.supplementalAccountKeysMask

    def getLinkedPublicKey(self) -> KeyDto:
        """Gets linked account public key.
        Returns:
            Linked account public key.
        """
        if not AccountKeyFlagsDto.LINKED in self.supplementalAccountKeysMask:
            raise Exception('supplementalAccountKeysMask is not set to LINKED.')
        return self.linkedPublicKey

    def getVrfPublicKey(self) -> KeyDto:
        """Gets vrf public key.
        Returns:
            Vrf public key.
        """
        if not AccountKeyFlagsDto.VRF in self.supplementalAccountKeysMask:
            raise Exception('supplementalAccountKeysMask is not set to VRF.')
        return self.vrfPublicKey

    def getVotingPublicKey(self) -> VotingKeyDto:
        """Gets voting public key.
        Returns:
            Voting public key.
        """
        if not AccountKeyFlagsDto.VOTING in self.supplementalAccountKeysMask:
            raise Exception('supplementalAccountKeysMask is not set to VOTING.')
        return self.votingPublicKey

    def getNodePublicKey(self) -> KeyDto:
        """Gets node public key.
        Returns:
            Node public key.
        """
        if not AccountKeyFlagsDto.NODE in self.supplementalAccountKeysMask:
            raise Exception('supplementalAccountKeysMask is not set to NODE.')
        return self.nodePublicKey

    def getImportanceSnapshots(self) -> ImportanceSnapshotBuilder:
        """Gets current importance snapshot of the account.
        Returns:
            Current importance snapshot of the account.
        """
        if not self.format == AccountStateFormatDto.HIGH_VALUE:
            raise Exception('format is not set to HIGH_VALUE.')
        return self.importanceSnapshots

    def getActivityBuckets(self) -> HeightActivityBucketsBuilder:
        """Gets activity buckets of the account.
        Returns:
            Activity buckets of the account.
        """
        if not self.format == AccountStateFormatDto.HIGH_VALUE:
            raise Exception('format is not set to HIGH_VALUE.')
        return self.activityBuckets

    def getCurrencyMosaicId(self) -> MosaicIdDto:
        """Gets currency mosaic id.
        Returns:
            Currency mosaic id.
        """
        return self.currencyMosaicId

    def getBalances(self) -> List[MosaicBuilder]:
        """Gets balances of account.
        Returns:
            Balances of account.
        """
        return self.balances

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.address.getSize()
        size += self.addressHeight.getSize()
        size += self.publicKey.getSize()
        size += self.publicKeyHeight.getSize()
        size += self.accountType.getSize()
        size += self.format.getSize()
        size += 1  # supplementalAccountKeysMask
        if AccountKeyFlagsDto.LINKED in self.supplementalAccountKeysMask:
            size += self.linkedPublicKey.getSize()
        if AccountKeyFlagsDto.VRF in self.supplementalAccountKeysMask:
            size += self.vrfPublicKey.getSize()
        if AccountKeyFlagsDto.VOTING in self.supplementalAccountKeysMask:
            size += self.votingPublicKey.getSize()
        if AccountKeyFlagsDto.NODE in self.supplementalAccountKeysMask:
            size += self.nodePublicKey.getSize()
        if self.format == AccountStateFormatDto.HIGH_VALUE:
            size += self.importanceSnapshots.getSize()
        if self.format == AccountStateFormatDto.HIGH_VALUE:
            size += self.activityBuckets.getSize()
        size += self.currencyMosaicId.getSize()
        size += 2  # balancesCount
        for _ in self.balances:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.address.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.addressHeight.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.publicKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.publicKeyHeight.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.accountType.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.format.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, AccountKeyFlagsDto.flagsToInt(self.getSupplementalAccountKeysMask()))  # kind:FLAGS
        if AccountKeyFlagsDto.LINKED in self.supplementalAccountKeysMask:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.linkedPublicKey.serialize())  # kind:CUSTOM
        if AccountKeyFlagsDto.VRF in self.supplementalAccountKeysMask:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.vrfPublicKey.serialize())  # kind:CUSTOM
        if AccountKeyFlagsDto.VOTING in self.supplementalAccountKeysMask:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.votingPublicKey.serialize())  # kind:CUSTOM
        if AccountKeyFlagsDto.NODE in self.supplementalAccountKeysMask:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.nodePublicKey.serialize())  # kind:CUSTOM
        if self.format == AccountStateFormatDto.HIGH_VALUE:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.importanceSnapshots.serialize())  # kind:CUSTOM
        if self.format == AccountStateFormatDto.HIGH_VALUE:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.activityBuckets.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.currencyMosaicId.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getBalances()), 2))  # kind:SIZE_FIELD
        for _ in self.balances:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())  # kind:ARRAY|VAR_ARRAY|FILL_ARRAY
        return bytes_
