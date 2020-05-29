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
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .Hash256Dto import Hash256Dto
from .KeyDto import KeyDto
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .NetworkTypeDto import NetworkTypeDto
from .SecretProofTransactionBodyBuilder import SecretProofTransactionBodyBuilder
from .UnresolvedAddressDto import UnresolvedAddressDto


class EmbeddedSecretProofTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded secret proof transaction.

    Attributes:
        secretProofTransactionBody: Secret proof transaction body.
    """

    def __init__(self, size: int, signerPublicKey: KeyDto, version: int, network: NetworkTypeDto, type: EntityTypeDto, secret: Hash256Dto, hashAlgorithm: LockHashAlgorithmDto, recipientAddress: UnresolvedAddressDto, proof: bytes):
        """Constructor.
        Args:
            size: Entity size.
            signerPublicKey: Entity signer's public key.
            version: Entity version.
            network: Entity network.
            type: Entity type.
            secret: Secret.
            hashAlgorithm: Hash algorithm.
            recipientAddress: Locked mosaic recipient address.
            proof: Proof data.
        """
        super().__init__(size, signerPublicKey, version, network, type)
        self.secretProofTransactionBody = SecretProofTransactionBodyBuilder(secret, hashAlgorithm, recipientAddress, proof)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedSecretProofTransactionBuilder:
        """Creates an instance of EmbeddedSecretProofTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedSecretProofTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]
        secretProofTransactionBody = SecretProofTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[secretProofTransactionBody.getSize():]
        return EmbeddedSecretProofTransactionBuilder(superObject.size, superObject.signerPublicKey, superObject.version, superObject.network, superObject.type, secretProofTransactionBody.secret, secretProofTransactionBody.hashAlgorithm, secretProofTransactionBody.recipientAddress, secretProofTransactionBody.proof)

    def getSecret(self) -> Hash256Dto:
        """Gets secret.
        Returns:
            Secret.
        """
        return self.secretProofTransactionBody.getSecret()

    def getHashAlgorithm(self) -> LockHashAlgorithmDto:
        """Gets hash algorithm.
        Returns:
            Hash algorithm.
        """
        return self.secretProofTransactionBody.getHashAlgorithm()

    def getRecipientAddress(self) -> UnresolvedAddressDto:
        """Gets locked mosaic recipient address.
        Returns:
            Locked mosaic recipient address.
        """
        return self.secretProofTransactionBody.getRecipientAddress()

    def getProof(self) -> bytes:
        """Gets proof data.
        Returns:
            Proof data.
        """
        return self.secretProofTransactionBody.getProof()

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.secretProofTransactionBody.getSize()
        return size

    def getBody(self) -> SecretProofTransactionBodyBuilder:
        """Gets the body builder of the object.
        Returns:
            Body builder.
        """
        return self.secretProofTransactionBody

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.secretProofTransactionBody.serialize())  # kind:CUSTOM
        return bytes_
