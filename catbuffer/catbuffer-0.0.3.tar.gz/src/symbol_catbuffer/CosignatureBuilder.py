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
from .KeyDto import KeyDto
from .SignatureDto import SignatureDto


class CosignatureBuilder:
    """Cosignature attached to an aggregate transaction.

    Attributes:
        signerPublicKey: Cosigner public key.
        signature: Cosigner signature.
    """

    def __init__(self, signerPublicKey: KeyDto, signature: SignatureDto):
        """Constructor.
        Args:
            signerPublicKey: Cosigner public key.
            signature: Cosigner signature.
        """
        self.signerPublicKey = signerPublicKey
        self.signature = signature

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> CosignatureBuilder:
        """Creates an instance of CosignatureBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of CosignatureBuilder.
        """
        bytes_ = bytes(payload)
        signerPublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[signerPublicKey.getSize():]
        signature = SignatureDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[signature.getSize():]
        return CosignatureBuilder(signerPublicKey, signature)

    def getSignerPublicKey(self) -> KeyDto:
        """Gets cosigner public key.
        Returns:
            Cosigner public key.
        """
        return self.signerPublicKey

    def getSignature(self) -> SignatureDto:
        """Gets cosigner signature.
        Returns:
            Cosigner signature.
        """
        return self.signature

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.signerPublicKey.getSize()
        size += self.signature.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.signerPublicKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.signature.serialize())  # kind:CUSTOM
        return bytes_
