"""Ocean module."""
#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import logging

from ocean_keeper.account import Account

from squid_py.secret_store.secret_store_provider import SecretStoreProvider

logger = logging.getLogger(__name__)


class OceanSecretStore:
    """Ocean SecretStore class."""

    def __init__(self, config):
        self._config = config
        if config.secret_store_url and config.parity_url and config.parity_address:
            logger.debug(f'\tSecretStore: url {config.secret_store_url}, '
                         f'parity-client {config.parity_url}, '
                         f'account {config.parity_address}')

        self._secret_store_url = config.secret_store_url
        self._parity_url = config.parity_url
        if config.parity_address and config.parity_password:
            self._account = Account(config.parity_address, config.parity_password, encrypted_key='{}')
            assert self._account.address and self._account.password, 'password for parity account is required.'

        else:
            logger.warning(f'The secretstore account is not initialized (parity.address '
                           f'and parity.password were not found in the config file). Make '
                           f'sure to set the account address and password using `set_account` '
                           f'before using the secretstore instance.')

    def _secret_store(self, account):
        return SecretStoreProvider.get_secret_store(
            self._secret_store_url,
            self._parity_url,
            account or self._account
        )

    def set_account(self, address, password):
        self._account = Account(address, password, encrypted_key='{}')

    def encrypt(self, document_id, content, account):
        """
        Encrypt string data using the DID as an secret store id,
        if secret store is enabled then return the result from secret store encryption

        None for no encryption performed

        :param document_id: hex str id of document to use for encryption session
        :param content: str to be encrypted
        :param account: Account instance encrypting this content
        :return: hex str encrypted content
        """
        return self._secret_store(account).encrypt_document(document_id, content)

    def decrypt(self, document_id, encrypted_content, account):
        """
        Decrypt a previously encrypted content using the secret store keys identified
        by document_id.

        Note that decryption requires permission already granted to the consumer account.

        :param document_id: hex str id of document to use to retrieve the decryption keys
        :param encrypted_content: hex str
        :param account: Account instance to use for decrypting the `encrypted_content`
        :return: str original content
        """
        return self._secret_store(account).decrypt_document(document_id, encrypted_content)
