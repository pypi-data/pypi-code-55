# coding: utf-8

# flake8: noqa

"""
    ****************************************************************************
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
    ****************************************************************************
    
    Catapult REST Endpoints
    OpenAPI Specification of catapult-rest 1.0.20.34  # noqa: E501
    The version of the OpenAPI document: 0.8.10
    Contact: ravi@nem.foundation

    NOTE: This file is auto generated by Symbol OpenAPI Generator:
    https://github.com/nemtech/symbol-openapi-generator
    Do not edit this file manually.
"""


from __future__ import absolute_import

__version__ = "0.8.10"

# import apis into sdk package
from symbol_openapi_client.api.account_routes_api import AccountRoutesApi
from symbol_openapi_client.api.block_routes_api import BlockRoutesApi
from symbol_openapi_client.api.chain_routes_api import ChainRoutesApi
from symbol_openapi_client.api.metadata_routes_api import MetadataRoutesApi
from symbol_openapi_client.api.mosaic_routes_api import MosaicRoutesApi
from symbol_openapi_client.api.multisig_routes_api import MultisigRoutesApi
from symbol_openapi_client.api.namespace_routes_api import NamespaceRoutesApi
from symbol_openapi_client.api.network_routes_api import NetworkRoutesApi
from symbol_openapi_client.api.node_routes_api import NodeRoutesApi
from symbol_openapi_client.api.receipt_routes_api import ReceiptRoutesApi
from symbol_openapi_client.api.restriction_account_routes_api import RestrictionAccountRoutesApi
from symbol_openapi_client.api.restriction_mosaic_routes_api import RestrictionMosaicRoutesApi
from symbol_openapi_client.api.transaction_routes_api import TransactionRoutesApi

# import ApiClient
from symbol_openapi_client.api_client import ApiClient
from symbol_openapi_client.configuration import Configuration
from symbol_openapi_client.exceptions import OpenApiException
from symbol_openapi_client.exceptions import ApiTypeError
from symbol_openapi_client.exceptions import ApiValueError
from symbol_openapi_client.exceptions import ApiKeyError
from symbol_openapi_client.exceptions import ApiException
# import models into sdk package
from symbol_openapi_client.models.account_address_restriction_transaction_body_dto import AccountAddressRestrictionTransactionBodyDTO
from symbol_openapi_client.models.account_address_restriction_transaction_dto import AccountAddressRestrictionTransactionDTO
from symbol_openapi_client.models.account_dto import AccountDTO
from symbol_openapi_client.models.account_ids import AccountIds
from symbol_openapi_client.models.account_info_dto import AccountInfoDTO
from symbol_openapi_client.models.account_key_dto import AccountKeyDTO
from symbol_openapi_client.models.account_key_link_network_properties_dto import AccountKeyLinkNetworkPropertiesDTO
from symbol_openapi_client.models.account_key_link_transaction_body_dto import AccountKeyLinkTransactionBodyDTO
from symbol_openapi_client.models.account_key_link_transaction_dto import AccountKeyLinkTransactionDTO
from symbol_openapi_client.models.account_metadata_transaction_body_dto import AccountMetadataTransactionBodyDTO
from symbol_openapi_client.models.account_metadata_transaction_dto import AccountMetadataTransactionDTO
from symbol_openapi_client.models.account_mosaic_restriction_transaction_body_dto import AccountMosaicRestrictionTransactionBodyDTO
from symbol_openapi_client.models.account_mosaic_restriction_transaction_dto import AccountMosaicRestrictionTransactionDTO
from symbol_openapi_client.models.account_names_dto import AccountNamesDTO
from symbol_openapi_client.models.account_operation_restriction_transaction_body_dto import AccountOperationRestrictionTransactionBodyDTO
from symbol_openapi_client.models.account_operation_restriction_transaction_dto import AccountOperationRestrictionTransactionDTO
from symbol_openapi_client.models.account_restriction_dto import AccountRestrictionDTO
from symbol_openapi_client.models.account_restriction_flags_enum import AccountRestrictionFlagsEnum
from symbol_openapi_client.models.account_restriction_network_properties_dto import AccountRestrictionNetworkPropertiesDTO
from symbol_openapi_client.models.account_restrictions_dto import AccountRestrictionsDTO
from symbol_openapi_client.models.account_restrictions_info_dto import AccountRestrictionsInfoDTO
from symbol_openapi_client.models.account_type_enum import AccountTypeEnum
from symbol_openapi_client.models.accounts_names_dto import AccountsNamesDTO
from symbol_openapi_client.models.activity_bucket_dto import ActivityBucketDTO
from symbol_openapi_client.models.address_alias_transaction_body_dto import AddressAliasTransactionBodyDTO
from symbol_openapi_client.models.address_alias_transaction_dto import AddressAliasTransactionDTO
from symbol_openapi_client.models.aggregate_network_properties_dto import AggregateNetworkPropertiesDTO
from symbol_openapi_client.models.aggregate_transaction_body_dto import AggregateTransactionBodyDTO
from symbol_openapi_client.models.aggregate_transaction_dto import AggregateTransactionDTO
from symbol_openapi_client.models.alias_action_enum import AliasActionEnum
from symbol_openapi_client.models.alias_dto import AliasDTO
from symbol_openapi_client.models.alias_type_enum import AliasTypeEnum
from symbol_openapi_client.models.announce_transaction_info_dto import AnnounceTransactionInfoDTO
from symbol_openapi_client.models.balance_change_receipt_dto import BalanceChangeReceiptDTO
from symbol_openapi_client.models.balance_change_receipt_dto_all_of import BalanceChangeReceiptDTOAllOf
from symbol_openapi_client.models.balance_transfer_receipt_dto import BalanceTransferReceiptDTO
from symbol_openapi_client.models.balance_transfer_receipt_dto_all_of import BalanceTransferReceiptDTOAllOf
from symbol_openapi_client.models.block_dto import BlockDTO
from symbol_openapi_client.models.block_dto_all_of import BlockDTOAllOf
from symbol_openapi_client.models.block_info_dto import BlockInfoDTO
from symbol_openapi_client.models.block_meta_dto import BlockMetaDTO
from symbol_openapi_client.models.chain_properties_dto import ChainPropertiesDTO
from symbol_openapi_client.models.chain_score_dto import ChainScoreDTO
from symbol_openapi_client.models.communication_timestamps_dto import CommunicationTimestampsDTO
from symbol_openapi_client.models.cosignature import Cosignature
from symbol_openapi_client.models.cosignature_dto import CosignatureDTO
from symbol_openapi_client.models.cosignature_dto_all_of import CosignatureDTOAllOf
from symbol_openapi_client.models.embedded_account_address_restriction_transaction_dto import EmbeddedAccountAddressRestrictionTransactionDTO
from symbol_openapi_client.models.embedded_account_key_link_transaction_dto import EmbeddedAccountKeyLinkTransactionDTO
from symbol_openapi_client.models.embedded_account_metadata_transaction_dto import EmbeddedAccountMetadataTransactionDTO
from symbol_openapi_client.models.embedded_account_mosaic_restriction_transaction_dto import EmbeddedAccountMosaicRestrictionTransactionDTO
from symbol_openapi_client.models.embedded_account_operation_restriction_transaction_dto import EmbeddedAccountOperationRestrictionTransactionDTO
from symbol_openapi_client.models.embedded_address_alias_transaction_dto import EmbeddedAddressAliasTransactionDTO
from symbol_openapi_client.models.embedded_hash_lock_transaction_dto import EmbeddedHashLockTransactionDTO
from symbol_openapi_client.models.embedded_mosaic_address_restriction_transaction_dto import EmbeddedMosaicAddressRestrictionTransactionDTO
from symbol_openapi_client.models.embedded_mosaic_alias_transaction_dto import EmbeddedMosaicAliasTransactionDTO
from symbol_openapi_client.models.embedded_mosaic_definition_transaction_dto import EmbeddedMosaicDefinitionTransactionDTO
from symbol_openapi_client.models.embedded_mosaic_global_restriction_transaction_dto import EmbeddedMosaicGlobalRestrictionTransactionDTO
from symbol_openapi_client.models.embedded_mosaic_metadata_transaction_dto import EmbeddedMosaicMetadataTransactionDTO
from symbol_openapi_client.models.embedded_mosaic_supply_change_transaction_dto import EmbeddedMosaicSupplyChangeTransactionDTO
from symbol_openapi_client.models.embedded_multisig_account_modification_transaction_dto import EmbeddedMultisigAccountModificationTransactionDTO
from symbol_openapi_client.models.embedded_namespace_metadata_transaction_dto import EmbeddedNamespaceMetadataTransactionDTO
from symbol_openapi_client.models.embedded_namespace_registration_transaction_dto import EmbeddedNamespaceRegistrationTransactionDTO
from symbol_openapi_client.models.embedded_node_key_link_transaction_dto import EmbeddedNodeKeyLinkTransactionDTO
from symbol_openapi_client.models.embedded_secret_lock_transaction_dto import EmbeddedSecretLockTransactionDTO
from symbol_openapi_client.models.embedded_secret_proof_transaction_dto import EmbeddedSecretProofTransactionDTO
from symbol_openapi_client.models.embedded_transaction_dto import EmbeddedTransactionDTO
from symbol_openapi_client.models.embedded_transaction_info_dto import EmbeddedTransactionInfoDTO
from symbol_openapi_client.models.embedded_transaction_meta_dto import EmbeddedTransactionMetaDTO
from symbol_openapi_client.models.embedded_transfer_transaction_dto import EmbeddedTransferTransactionDTO
from symbol_openapi_client.models.embedded_voting_key_link_transaction_dto import EmbeddedVotingKeyLinkTransactionDTO
from symbol_openapi_client.models.embedded_vrf_key_link_transaction_dto import EmbeddedVrfKeyLinkTransactionDTO
from symbol_openapi_client.models.entity_dto import EntityDTO
from symbol_openapi_client.models.hash_lock_network_properties_dto import HashLockNetworkPropertiesDTO
from symbol_openapi_client.models.hash_lock_transaction_body_dto import HashLockTransactionBodyDTO
from symbol_openapi_client.models.hash_lock_transaction_dto import HashLockTransactionDTO
from symbol_openapi_client.models.height_info_dto import HeightInfoDTO
from symbol_openapi_client.models.inflation_receipt_dto import InflationReceiptDTO
from symbol_openapi_client.models.inflation_receipt_dto_all_of import InflationReceiptDTOAllOf
from symbol_openapi_client.models.key_type_enum import KeyTypeEnum
from symbol_openapi_client.models.link_action_enum import LinkActionEnum
from symbol_openapi_client.models.lock_hash_algorithm_enum import LockHashAlgorithmEnum
from symbol_openapi_client.models.merkle_path_item_dto import MerklePathItemDTO
from symbol_openapi_client.models.merkle_proof_info_dto import MerkleProofInfoDTO
from symbol_openapi_client.models.message_dto import MessageDTO
from symbol_openapi_client.models.message_type_enum import MessageTypeEnum
from symbol_openapi_client.models.metadata_dto import MetadataDTO
from symbol_openapi_client.models.metadata_entries_dto import MetadataEntriesDTO
from symbol_openapi_client.models.metadata_entry_dto import MetadataEntryDTO
from symbol_openapi_client.models.metadata_network_properties_dto import MetadataNetworkPropertiesDTO
from symbol_openapi_client.models.metadata_type_enum import MetadataTypeEnum
from symbol_openapi_client.models.model_error import ModelError
from symbol_openapi_client.models.mosaic import Mosaic
from symbol_openapi_client.models.mosaic_address_restriction_dto import MosaicAddressRestrictionDTO
from symbol_openapi_client.models.mosaic_address_restriction_entry_dto import MosaicAddressRestrictionEntryDTO
from symbol_openapi_client.models.mosaic_address_restriction_entry_wrapper_dto import MosaicAddressRestrictionEntryWrapperDTO
from symbol_openapi_client.models.mosaic_address_restriction_transaction_body_dto import MosaicAddressRestrictionTransactionBodyDTO
from symbol_openapi_client.models.mosaic_address_restriction_transaction_dto import MosaicAddressRestrictionTransactionDTO
from symbol_openapi_client.models.mosaic_alias_transaction_body_dto import MosaicAliasTransactionBodyDTO
from symbol_openapi_client.models.mosaic_alias_transaction_dto import MosaicAliasTransactionDTO
from symbol_openapi_client.models.mosaic_dto import MosaicDTO
from symbol_openapi_client.models.mosaic_definition_transaction_body_dto import MosaicDefinitionTransactionBodyDTO
from symbol_openapi_client.models.mosaic_definition_transaction_dto import MosaicDefinitionTransactionDTO
from symbol_openapi_client.models.mosaic_expiry_receipt_dto import MosaicExpiryReceiptDTO
from symbol_openapi_client.models.mosaic_expiry_receipt_dto_all_of import MosaicExpiryReceiptDTOAllOf
from symbol_openapi_client.models.mosaic_global_restriction_dto import MosaicGlobalRestrictionDTO
from symbol_openapi_client.models.mosaic_global_restriction_entry_dto import MosaicGlobalRestrictionEntryDTO
from symbol_openapi_client.models.mosaic_global_restriction_entry_restriction_dto import MosaicGlobalRestrictionEntryRestrictionDTO
from symbol_openapi_client.models.mosaic_global_restriction_entry_wrapper_dto import MosaicGlobalRestrictionEntryWrapperDTO
from symbol_openapi_client.models.mosaic_global_restriction_transaction_body_dto import MosaicGlobalRestrictionTransactionBodyDTO
from symbol_openapi_client.models.mosaic_global_restriction_transaction_dto import MosaicGlobalRestrictionTransactionDTO
from symbol_openapi_client.models.mosaic_ids import MosaicIds
from symbol_openapi_client.models.mosaic_info_dto import MosaicInfoDTO
from symbol_openapi_client.models.mosaic_metadata_transaction_body_dto import MosaicMetadataTransactionBodyDTO
from symbol_openapi_client.models.mosaic_metadata_transaction_dto import MosaicMetadataTransactionDTO
from symbol_openapi_client.models.mosaic_names_dto import MosaicNamesDTO
from symbol_openapi_client.models.mosaic_network_properties_dto import MosaicNetworkPropertiesDTO
from symbol_openapi_client.models.mosaic_restriction_entry_type_enum import MosaicRestrictionEntryTypeEnum
from symbol_openapi_client.models.mosaic_restriction_network_properties_dto import MosaicRestrictionNetworkPropertiesDTO
from symbol_openapi_client.models.mosaic_restriction_type_enum import MosaicRestrictionTypeEnum
from symbol_openapi_client.models.mosaic_supply_change_action_enum import MosaicSupplyChangeActionEnum
from symbol_openapi_client.models.mosaic_supply_change_transaction_body_dto import MosaicSupplyChangeTransactionBodyDTO
from symbol_openapi_client.models.mosaic_supply_change_transaction_dto import MosaicSupplyChangeTransactionDTO
from symbol_openapi_client.models.mosaics_info_dto import MosaicsInfoDTO
from symbol_openapi_client.models.mosaics_names_dto import MosaicsNamesDTO
from symbol_openapi_client.models.multisig_account_graph_info_dto import MultisigAccountGraphInfoDTO
from symbol_openapi_client.models.multisig_account_info_dto import MultisigAccountInfoDTO
from symbol_openapi_client.models.multisig_account_modification_transaction_body_dto import MultisigAccountModificationTransactionBodyDTO
from symbol_openapi_client.models.multisig_account_modification_transaction_dto import MultisigAccountModificationTransactionDTO
from symbol_openapi_client.models.multisig_dto import MultisigDTO
from symbol_openapi_client.models.multisig_network_properties_dto import MultisigNetworkPropertiesDTO
from symbol_openapi_client.models.namespace_dto import NamespaceDTO
from symbol_openapi_client.models.namespace_expiry_receipt_dto import NamespaceExpiryReceiptDTO
from symbol_openapi_client.models.namespace_expiry_receipt_dto_all_of import NamespaceExpiryReceiptDTOAllOf
from symbol_openapi_client.models.namespace_ids import NamespaceIds
from symbol_openapi_client.models.namespace_info_dto import NamespaceInfoDTO
from symbol_openapi_client.models.namespace_meta_dto import NamespaceMetaDTO
from symbol_openapi_client.models.namespace_metadata_transaction_body_dto import NamespaceMetadataTransactionBodyDTO
from symbol_openapi_client.models.namespace_metadata_transaction_dto import NamespaceMetadataTransactionDTO
from symbol_openapi_client.models.namespace_name_dto import NamespaceNameDTO
from symbol_openapi_client.models.namespace_network_properties_dto import NamespaceNetworkPropertiesDTO
from symbol_openapi_client.models.namespace_registration_transaction_body_dto import NamespaceRegistrationTransactionBodyDTO
from symbol_openapi_client.models.namespace_registration_transaction_dto import NamespaceRegistrationTransactionDTO
from symbol_openapi_client.models.namespace_registration_type_enum import NamespaceRegistrationTypeEnum
from symbol_openapi_client.models.namespaces_info_dto import NamespacesInfoDTO
from symbol_openapi_client.models.network_configuration_dto import NetworkConfigurationDTO
from symbol_openapi_client.models.network_properties_dto import NetworkPropertiesDTO
from symbol_openapi_client.models.network_type_dto import NetworkTypeDTO
from symbol_openapi_client.models.network_type_enum import NetworkTypeEnum
from symbol_openapi_client.models.node_health_dto import NodeHealthDTO
from symbol_openapi_client.models.node_health_info_dto import NodeHealthInfoDTO
from symbol_openapi_client.models.node_identity_equality_strategy import NodeIdentityEqualityStrategy
from symbol_openapi_client.models.node_info_dto import NodeInfoDTO
from symbol_openapi_client.models.node_key_link_network_properties_dto import NodeKeyLinkNetworkPropertiesDTO
from symbol_openapi_client.models.node_key_link_transaction_body_dto import NodeKeyLinkTransactionBodyDTO
from symbol_openapi_client.models.node_key_link_transaction_dto import NodeKeyLinkTransactionDTO
from symbol_openapi_client.models.node_status_enum import NodeStatusEnum
from symbol_openapi_client.models.node_time_dto import NodeTimeDTO
from symbol_openapi_client.models.plugins_properties_dto import PluginsPropertiesDTO
from symbol_openapi_client.models.position_enum import PositionEnum
from symbol_openapi_client.models.receipt_dto import ReceiptDTO
from symbol_openapi_client.models.receipt_type_enum import ReceiptTypeEnum
from symbol_openapi_client.models.rental_fees_dto import RentalFeesDTO
from symbol_openapi_client.models.resolution_entry_dto import ResolutionEntryDTO
from symbol_openapi_client.models.resolution_statement_body_dto import ResolutionStatementBodyDTO
from symbol_openapi_client.models.resolution_statement_dto import ResolutionStatementDTO
from symbol_openapi_client.models.roles_type_enum import RolesTypeEnum
from symbol_openapi_client.models.secret_lock_network_properties_dto import SecretLockNetworkPropertiesDTO
from symbol_openapi_client.models.secret_lock_transaction_body_dto import SecretLockTransactionBodyDTO
from symbol_openapi_client.models.secret_lock_transaction_dto import SecretLockTransactionDTO
from symbol_openapi_client.models.secret_proof_transaction_body_dto import SecretProofTransactionBodyDTO
from symbol_openapi_client.models.secret_proof_transaction_dto import SecretProofTransactionDTO
from symbol_openapi_client.models.server_dto import ServerDTO
from symbol_openapi_client.models.server_info_dto import ServerInfoDTO
from symbol_openapi_client.models.source_dto import SourceDTO
from symbol_openapi_client.models.statements_dto import StatementsDTO
from symbol_openapi_client.models.storage_info_dto import StorageInfoDTO
from symbol_openapi_client.models.transaction_body_dto import TransactionBodyDTO
from symbol_openapi_client.models.transaction_dto import TransactionDTO
from symbol_openapi_client.models.transaction_fees_dto import TransactionFeesDTO
from symbol_openapi_client.models.transaction_hashes import TransactionHashes
from symbol_openapi_client.models.transaction_ids import TransactionIds
from symbol_openapi_client.models.transaction_info_dto import TransactionInfoDTO
from symbol_openapi_client.models.transaction_meta_dto import TransactionMetaDTO
from symbol_openapi_client.models.transaction_payload import TransactionPayload
from symbol_openapi_client.models.transaction_state_type_enum import TransactionStateTypeEnum
from symbol_openapi_client.models.transaction_statement_body_dto import TransactionStatementBodyDTO
from symbol_openapi_client.models.transaction_statement_dto import TransactionStatementDTO
from symbol_openapi_client.models.transaction_status_dto import TransactionStatusDTO
from symbol_openapi_client.models.transaction_status_type_enum import TransactionStatusTypeEnum
from symbol_openapi_client.models.transaction_type_enum import TransactionTypeEnum
from symbol_openapi_client.models.transfer_network_properties_dto import TransferNetworkPropertiesDTO
from symbol_openapi_client.models.transfer_transaction_body_dto import TransferTransactionBodyDTO
from symbol_openapi_client.models.transfer_transaction_dto import TransferTransactionDTO
from symbol_openapi_client.models.unresolved_mosaic import UnresolvedMosaic
from symbol_openapi_client.models.verifiable_entity_dto import VerifiableEntityDTO
from symbol_openapi_client.models.voting_key_link_network_properties_dto import VotingKeyLinkNetworkPropertiesDTO
from symbol_openapi_client.models.voting_key_link_transaction_body_dto import VotingKeyLinkTransactionBodyDTO
from symbol_openapi_client.models.voting_key_link_transaction_dto import VotingKeyLinkTransactionDTO
from symbol_openapi_client.models.vrf_key_link_network_properties_dto import VrfKeyLinkNetworkPropertiesDTO
from symbol_openapi_client.models.vrf_key_link_transaction_body_dto import VrfKeyLinkTransactionBodyDTO
from symbol_openapi_client.models.vrf_key_link_transaction_dto import VrfKeyLinkTransactionDTO

