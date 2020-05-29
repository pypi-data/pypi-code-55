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

# pylint: disable=R0911,R0912

# Imports for creating embedded transaction builders
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EmbeddedAccountAddressRestrictionTransactionBuilder import EmbeddedAccountAddressRestrictionTransactionBuilder
from .EmbeddedAccountKeyLinkTransactionBuilder import EmbeddedAccountKeyLinkTransactionBuilder
from .EmbeddedAccountMetadataTransactionBuilder import EmbeddedAccountMetadataTransactionBuilder
from .EmbeddedAccountMosaicRestrictionTransactionBuilder import EmbeddedAccountMosaicRestrictionTransactionBuilder
from .EmbeddedAccountOperationRestrictionTransactionBuilder import EmbeddedAccountOperationRestrictionTransactionBuilder
from .EmbeddedAddressAliasTransactionBuilder import EmbeddedAddressAliasTransactionBuilder
from .EmbeddedHashLockTransactionBuilder import EmbeddedHashLockTransactionBuilder
from .EmbeddedMosaicAddressRestrictionTransactionBuilder import EmbeddedMosaicAddressRestrictionTransactionBuilder
from .EmbeddedMosaicAliasTransactionBuilder import EmbeddedMosaicAliasTransactionBuilder
from .EmbeddedMosaicDefinitionTransactionBuilder import EmbeddedMosaicDefinitionTransactionBuilder
from .EmbeddedMosaicGlobalRestrictionTransactionBuilder import EmbeddedMosaicGlobalRestrictionTransactionBuilder
from .EmbeddedMosaicMetadataTransactionBuilder import EmbeddedMosaicMetadataTransactionBuilder
from .EmbeddedMosaicSupplyChangeTransactionBuilder import EmbeddedMosaicSupplyChangeTransactionBuilder
from .EmbeddedMultisigAccountModificationTransactionBuilder import EmbeddedMultisigAccountModificationTransactionBuilder
from .EmbeddedNamespaceMetadataTransactionBuilder import EmbeddedNamespaceMetadataTransactionBuilder
from .EmbeddedNamespaceRegistrationTransactionBuilder import EmbeddedNamespaceRegistrationTransactionBuilder
from .EmbeddedNodeKeyLinkTransactionBuilder import EmbeddedNodeKeyLinkTransactionBuilder
from .EmbeddedSecretLockTransactionBuilder import EmbeddedSecretLockTransactionBuilder
from .EmbeddedSecretProofTransactionBuilder import EmbeddedSecretProofTransactionBuilder
from .EmbeddedTransferTransactionBuilder import EmbeddedTransferTransactionBuilder
from .EmbeddedVotingKeyLinkTransactionBuilder import EmbeddedVotingKeyLinkTransactionBuilder
from .EmbeddedVrfKeyLinkTransactionBuilder import EmbeddedVrfKeyLinkTransactionBuilder
# Imports for creating transaction builders
from .TransactionBuilder import TransactionBuilder
from .AggregateBondedTransactionBuilder import AggregateBondedTransactionBuilder
from .AggregateCompleteTransactionBuilder import AggregateCompleteTransactionBuilder
from .AccountAddressRestrictionTransactionBuilder import AccountAddressRestrictionTransactionBuilder
from .AccountKeyLinkTransactionBuilder import AccountKeyLinkTransactionBuilder
from .AccountMetadataTransactionBuilder import AccountMetadataTransactionBuilder
from .AccountMosaicRestrictionTransactionBuilder import AccountMosaicRestrictionTransactionBuilder
from .AccountOperationRestrictionTransactionBuilder import AccountOperationRestrictionTransactionBuilder
from .AddressAliasTransactionBuilder import AddressAliasTransactionBuilder
from .HashLockTransactionBuilder import HashLockTransactionBuilder
from .MosaicAddressRestrictionTransactionBuilder import MosaicAddressRestrictionTransactionBuilder
from .MosaicAliasTransactionBuilder import MosaicAliasTransactionBuilder
from .MosaicDefinitionTransactionBuilder import MosaicDefinitionTransactionBuilder
from .MosaicGlobalRestrictionTransactionBuilder import MosaicGlobalRestrictionTransactionBuilder
from .MosaicMetadataTransactionBuilder import MosaicMetadataTransactionBuilder
from .MosaicSupplyChangeTransactionBuilder import MosaicSupplyChangeTransactionBuilder
from .MultisigAccountModificationTransactionBuilder import MultisigAccountModificationTransactionBuilder
from .NamespaceMetadataTransactionBuilder import NamespaceMetadataTransactionBuilder
from .NamespaceRegistrationTransactionBuilder import NamespaceRegistrationTransactionBuilder
from .NodeKeyLinkTransactionBuilder import NodeKeyLinkTransactionBuilder
from .SecretLockTransactionBuilder import SecretLockTransactionBuilder
from .SecretProofTransactionBuilder import SecretProofTransactionBuilder
from .TransferTransactionBuilder import TransferTransactionBuilder
from .VotingKeyLinkTransactionBuilder import VotingKeyLinkTransactionBuilder
from .VrfKeyLinkTransactionBuilder import VrfKeyLinkTransactionBuilder


class TransactionBuilderFactory:
    """Factory in charge of creating the specific transaction builder from the binary payload.

    It has 2 class methods:
    (i) createEmbeddedTransactionBuilder
            Creates the specific embedded transaction builder from given payload.
    (ii) createTransactionBuilder
            Creates the specific transaction builder from given payload.
    """

    @classmethod
    def createEmbeddedTransactionBuilder(cls, payload) -> EmbeddedTransactionBuilder:
        """
        It creates the specific embedded transaction builder from the payload bytes.
        Args:
            payload: bytes
        Returns:
            the EmbeddedTransactionBuilder subclass
        """
        headerBuilder = EmbeddedTransactionBuilder.loadFromBinary(payload)
        entityType = headerBuilder.getType().value
        if entityType == 16717:
            return EmbeddedMosaicDefinitionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16716:
            return EmbeddedAccountKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16972:
            return EmbeddedNodeKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16707:
            return EmbeddedVotingKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16963:
            return EmbeddedVrfKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16712:
            return EmbeddedHashLockTransactionBuilder.loadFromBinary(payload)
        if entityType == 16722:
            return EmbeddedSecretLockTransactionBuilder.loadFromBinary(payload)
        if entityType == 16978:
            return EmbeddedSecretProofTransactionBuilder.loadFromBinary(payload)
        if entityType == 16708:
            return EmbeddedAccountMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 16964:
            return EmbeddedMosaicMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 17220:
            return EmbeddedNamespaceMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 16973:
            return EmbeddedMosaicSupplyChangeTransactionBuilder.loadFromBinary(payload)
        if entityType == 16725:
            return EmbeddedMultisigAccountModificationTransactionBuilder.loadFromBinary(payload)
        if entityType == 16974:
            return EmbeddedAddressAliasTransactionBuilder.loadFromBinary(payload)
        if entityType == 17230:
            return EmbeddedMosaicAliasTransactionBuilder.loadFromBinary(payload)
        if entityType == 16718:
            return EmbeddedNamespaceRegistrationTransactionBuilder.loadFromBinary(payload)
        if entityType == 16720:
            return EmbeddedAccountAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16976:
            return EmbeddedAccountMosaicRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 17232:
            return EmbeddedAccountOperationRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16977:
            return EmbeddedMosaicAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16721:
            return EmbeddedMosaicGlobalRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16724:
            return EmbeddedTransferTransactionBuilder.loadFromBinary(payload)
        return headerBuilder

    @classmethod
    def createTransactionBuilder(cls, payload) -> TransactionBuilder:
        """
        It creates the specific transaction builder from the payload bytes.
        Args:
            payload: bytes
        Returns:
            the TransactionBuilder subclass
        """
        headerBuilder = TransactionBuilder.loadFromBinary(payload)
        entityType = headerBuilder.getType().value
        if entityType == 16717:
            return MosaicDefinitionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16716:
            return AccountKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16972:
            return NodeKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16705:
            return AggregateCompleteTransactionBuilder.loadFromBinary(payload)
        if entityType == 16961:
            return AggregateBondedTransactionBuilder.loadFromBinary(payload)
        if entityType == 16707:
            return VotingKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16963:
            return VrfKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 16712:
            return HashLockTransactionBuilder.loadFromBinary(payload)
        if entityType == 16722:
            return SecretLockTransactionBuilder.loadFromBinary(payload)
        if entityType == 16978:
            return SecretProofTransactionBuilder.loadFromBinary(payload)
        if entityType == 16708:
            return AccountMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 16964:
            return MosaicMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 17220:
            return NamespaceMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 16973:
            return MosaicSupplyChangeTransactionBuilder.loadFromBinary(payload)
        if entityType == 16725:
            return MultisigAccountModificationTransactionBuilder.loadFromBinary(payload)
        if entityType == 16974:
            return AddressAliasTransactionBuilder.loadFromBinary(payload)
        if entityType == 17230:
            return MosaicAliasTransactionBuilder.loadFromBinary(payload)
        if entityType == 16718:
            return NamespaceRegistrationTransactionBuilder.loadFromBinary(payload)
        if entityType == 16720:
            return AccountAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16976:
            return AccountMosaicRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 17232:
            return AccountOperationRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16977:
            return MosaicAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16721:
            return MosaicGlobalRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 16724:
            return TransferTransactionBuilder.loadFromBinary(payload)
        return headerBuilder
