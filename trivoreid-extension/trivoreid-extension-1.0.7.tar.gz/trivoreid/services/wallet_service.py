#!/usr/bin/env python
# coding: utf-8

import requests
import logging

import trivoreid.utils.service_utils as su
from trivoreid.utils.criteria import Filter
from trivoreid.models.wallet import *
from trivoreid.models.page import Page
from trivoreid.exceptions import TrivoreIDSDKException, TrivoreIDException

class WalletService(object):
    '''
    Class to wrap Trivore ID /wallet API
    '''

    _WALLETS = 'api/rest/v1/wallet'
    _WALLET = 'api/rest/v1/wallet/{}'
    _DEPOSIT = 'api/rest/v1/wallet/{}/deposit'
    _TRANSFER = 'api/rest/v1/wallet/{}/transfer'
    _WITHDRAW = 'api/rest/v1/wallet/{}/withdraw'

    def __init__(self, credentials):
        self._server = credentials.server

        if credentials.oidc_client is None:
            self._session = requests
            self._auth = credentials.auth
        else:
            self._session = credentials.oidc_client
            self._auth = None

        self._auth_header = credentials.access_token

    def get_all(self,
                filter_fields=None,
                start_index=0,
                count=100,
                sortBy=None,
                ascending=None):
        '''Get the list of the wallets.
        Args:
            filter_fields (Filter) : utils.Filter class to filter out
                                     the result.
            start_index (int)      : 0-based pagination start index
            count (int)            : pagination page size, max 500,
                                     100 by default
            sortBy (str)           : Sort by attribute name
            ascending (bool)       : Sort direction (ascending or descending)
        Returns:
            Page with the pagination data and the list of wallets.
        Raises:
            TrivoreIDException if the status code is not 200.
        '''
        params = su.generate_parameters(filter_fields, start_index, count)

        if sortBy != None:
            params['sortBy'] = sortBy

        if ascending != None:
            if ascending:
                params['ascending'] = 'ascending'
            else:
                params['ascending'] = 'descending'

        response = self._session.get(
                                su.uri(self._server, self._WALLETS),
                                params=params,
                                headers=self._auth_header,
                                auth=self._auth)

        if response.status_code == 200:
            logging.debug('Found {} wallets'.format(
                        len(response.json()['resources'])))

            ls = []
            for l in response.json()['resources']:
                ls.append(Wallet(l))
            page = Page(response.json(), ls)
            return page
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)

    def create(self, wallet):
        '''Create new wallet.
        Args:
            wallet (Wallet) : wallet to create.
        Returns:
            New wallet object.
        Raises:
            TrivoreIDSDKException if the type of the Wallet is wrong
            TrivoreIDException if the status code is not 201.
        '''
        if 'Wallet' not in str(type(wallet)):
            raise TrivoreIDSDKException('Wallet type is wrong!')

        response = self._session.post(su.uri(self._server, self._WALLETS),
                                      json=wallet.serialize(),
                                      headers=self._auth_header,
                                      auth=self._auth)

        if response.status_code == 201:
            wallet = Wallet(response.json())
            logging.debug('Successfully created wallet with id {}'
                                                    .format(wallet.id))
            return wallet
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)

    def get(self, walletId):
        '''Get the single wallet by id.
        Args:
            walletId (str) : wallet unique identifier
        Returns:
            A wallet.
        Raises:
            TrivoreIDException if the status code is not 200.
        '''
        uri = su.uri(self._server, self._WALLET).format(walletId)
        response = self._session.get(uri,
                                     headers=self._auth_header,
                                     auth=self._auth)

        if response.status_code is 200:
            logging.debug('Found wallet with id {}'.format(walletId))
            return Wallet(response.json())
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)

    def update(self, wallet, walletId=None):
        '''Modify a wallet.
        Args:
            wallet (Wallet) : wallet to modify.
            walletId (str)  : if None, then wallet ID from the Wallet object
                              will be used.
        Returns:
            Modified wallet object.
        Raises:
            TrivoreIDSDKException if the type of the Wallet is wrong
            TrivoreIDException if the status code is not 200.
        '''
        if 'Wallet' not in str(type(wallet)):
            raise TrivoreIDSDKException('Wallet type is wrong!')

        if walletId is None:
            walletId = wallet.id

        uri = su.uri(self._server, self._WALLET).format(walletId)
        response = self._session.put(uri,
                                     json=wallet.serialize(),
                                     headers=self._auth_header,
                                     auth=self._auth)

        if response.status_code is 200:
            logging.debug('Successfully modified wallet with the id {}'
                        .format(walletId))
            return Wallet(response.json())
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)

    def delete(self, walletId):
        '''Delete wallet by id.
        Args:
            walletId (str) : wallet unique identifier
        Raises:
            TrivoreIDException if the status code is not 204.
        '''
        uri = su.uri(self._server, self._WALLET).format(walletId)
        response = self._session.delete(uri,
                                        headers=self._auth_header,
                                        auth=self._auth)

        if response.status_code is 204:
            logging.debug('Successfully deleted wallet with id {}'
                                                    .format(walletId))
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)

    def deposit(self, walletId, transaction):
        '''Deposit funds to an account.
        Funds are not transferred from another wallet, they are simply added
        to the wallet.
        Args:
            walletId (str) : wallet unique identifier
            transaction (Transaction): transaction info
        Raises:
            TrivoreIDSDKException if the type of the Transaction is wrong
            TrivoreIDException if the status code is not 204.
        '''
        if 'Transaction' not in str(type(transaction)):
            raise TrivoreIDSDKException('Transaction type is wrong!')

        uri = su.uri(self._server, self._DEPOSIT).format(walletId)
        response = self._session.post(uri,
                                      json=transaction.serialize(),
                                      headers=self._auth_header,
                                      auth=self._auth)

        if response.status_code is 204:
            logging.debug('Successfully completed deposit to wallet {}'
                                                    .format(walletId))
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)

    def transfer(self, walletId, transaction):
        '''Transfer funds to another wallet.
        Only wallet owner, wallet holders, or those with read access to wallet
        and DEPOSIT and WITHDRAW permissions can transfer funds between wallets.
        Args:
            walletId (str) : wallet unique identifier
            transaction (Transaction): transaction info
        Raises:
            TrivoreIDSDKException if the type of the Transaction is wrong
            TrivoreIDException if the status code is not 204.
        '''
        if 'Transaction' not in str(type(transaction)):
            raise TrivoreIDSDKException('Transaction type is wrong!')

        uri = su.uri(self._server, self._TRANSFER).format(walletId)
        response = self._session.post(uri,
                                      json=transaction.serialize(),
                                      headers=self._auth_header,
                                      auth=self._auth)

        if response.status_code is 204:
            logging.debug('Successfully completed transfer to wallet {}'
                                                    .format(walletId))
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)

    def withdraw(self, walletId, transaction):
        '''Withdraw funds from a wallet.
        Funds are not transferred to another wallet, they are simply removed
        from source wallet.
        Args:
            walletId (str) : wallet unique identifier
            transaction (Transaction): transaction info
        Raises:
            TrivoreIDSDKException if the type of the Transaction is wrong
            TrivoreIDException if the status code is not 204.
        '''
        if 'Transaction' not in str(type(transaction)):
            raise TrivoreIDSDKException('Transaction type is wrong!')

        uri = su.uri(self._server, self._WITHDRAW).format(walletId)
        response = self._session.post(uri,
                                      json=transaction.serialize(),
                                      headers=self._auth_header,
                                      auth=self._auth)

        if response.status_code is 204:
            logging.debug('Successfully completed withdraw to wallet {}'
                                                    .format(walletId))
        else:
            raise TrivoreIDException(su.error_response_message(response),
                                     response.status_code)
