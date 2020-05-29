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
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .MultisigAccountModificationTransactionBodyBuilder import MultisigAccountModificationTransactionBodyBuilder
from .NetworkTypeDto import NetworkTypeDto


class EmbeddedMultisigAccountModificationTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded multisig account modification transaction.

    Attributes:
        multisigAccountModificationTransactionBody: Multisig account modification transaction body.
    """

    def __init__(self, size: int, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, minRemovalDelta: int, minApprovalDelta: int, publicKeyAdditions: List[KeyDto], publicKeyDeletions: List[KeyDto]):
        """Constructor.
        Args:
            size: Entity size.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            minRemovalDelta: Relative change of the minimal number of cosignatories required when removing an account.
            minApprovalDelta: Relative change of the minimal number of cosignatories required when approving a transaction.
            publicKeyAdditions: Cosignatory public key additions.
            publicKeyDeletions: Cosignatory public key deletions.
        """
        super().__init__(size, signerPublicKey, version, network, type)
        self.multisigAccountModificationTransactionBody = MultisigAccountModificationTransactionBodyBuilder(minRemovalDelta, minApprovalDelta, publicKeyAdditions, publicKeyDeletions)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedMultisigAccountModificationTransactionBuilder:
        """Creates an instance of EmbeddedMultisigAccountModificationTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedMultisigAccountModificationTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        multisigAccountModificationTransactionBody = MultisigAccountModificationTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[multisigAccountModificationTransactionBody.getSize():]
        return EmbeddedMultisigAccountModificationTransactionBuilder(superObject.size, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, multisigAccountModificationTransactionBody.minRemovalDelta, multisigAccountModificationTransactionBody.minApprovalDelta, multisigAccountModificationTransactionBody.publicKeyAdditions, multisigAccountModificationTransactionBody.publicKeyDeletions)

    def getMinRemovalDelta(self) -> int:
        """Gets relative change of the minimal number of cosignatories required when removing an account.
        Returns:
            Relative change of the minimal number of cosignatories required when removing an account.
        """
        return self.multisigAccountModificationTransactionBody.getMinRemovalDelta()

    def getMinApprovalDelta(self) -> int:
        """Gets relative change of the minimal number of cosignatories required when approving a transaction.
        Returns:
            Relative change of the minimal number of cosignatories required when approving a transaction.
        """
        return self.multisigAccountModificationTransactionBody.getMinApprovalDelta()

    def getPublicKeyAdditions(self) -> List[KeyDto]:
        """Gets cosignatory public key additions.
        Returns:
            Cosignatory public key additions.
        """
        return self.multisigAccountModificationTransactionBody.getPublicKeyAdditions()

    def getPublicKeyDeletions(self) -> List[KeyDto]:
        """Gets cosignatory public key deletions.
        Returns:
            Cosignatory public key deletions.
        """
        return self.multisigAccountModificationTransactionBody.getPublicKeyDeletions()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.multisigAccountModificationTransactionBody.getSize()
        return size

    def getBody(self) -> MultisigAccountModificationTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.multisigAccountModificationTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.multisigAccountModificationTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
