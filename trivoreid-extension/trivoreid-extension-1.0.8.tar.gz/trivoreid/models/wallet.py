#!/usr/bin/env python
# coding: utf-8

class Wallet(object):
    '''
    Class that represents a Wallet object.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict) : wallet fields
        Dictionary keys:
            'id' (str) Entity ID
            'balance' (str) Wallet balance
            'currency' (str) Wallet currency, ISO 4217 code. Unmodifiable after
                             wallet creation.
            'events' (list) list of WalletEvent objects. Wallet event history.
            'ownerId' (str) owner ID
            'holderIds' (list)  list of strings
            'accessControlIds' (list) list of strings
            'name' (str) Wallet name
            'identifiableNamespaceId' (str) Identifiable namespace ID
            'identifiableNamespace' (str) Identifiable namespace
            'identifiableName' (str) Identifiable name
        '''

        self.events = []
        for e in data.pop('events', []):
            self.events.append(WalletEvent(e))

        self.id = data.pop('id', None)
        self.balance = data.pop('balance', None)
        self.currency = data.pop('currency', None)
        self.ownerId = data.pop('ownerId', None)
        self.holderIds = data.pop('holderIds', [])
        self.accessControlIds = data.pop('accessControlIds', [])
        self.name = data.pop('name', None)
        self.identifiableNamespaceId = data.pop('identifiableNamespaceId', None)
        self.identifiableNamespace = data.pop('identifiableNamespace', None)
        self.identifiableName = data.pop('identifiableName', None)

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''

        events = []
        for e in self.events:
            events.append(e.serialize())

        return {
            'id'                        : self.id,
            'balance'                   : self.balance,
            'currency'                  : self.currency,
            'events'                    : events,
            'ownerId'                   : self.ownerId,
            'holderIds'                 : self.holderIds,
            'accessControlIds'          : self.accessControlIds,
            'name'                      : self.name,
            'identifiableNamespaceId'   : self.identifiableNamespaceId,
            'identifiableNamespace'     : self.identifiableNamespace,
            'identifiableName'          : self.identifiableName
        }

class WalletEvent(object):
    '''
    Class that represents a WalletEvent object.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict) : wallet event fields
        Dictionary keys:
            'id' (str)
            'time' (str)
            'balanceChange' (float)
            'message' (str)
            'transferTo' (str)
            'transferFrom' (str)
        '''
        self.id = data.pop('id', None)
        self.time = data.pop('time', None)
        self.balanceChange = data.pop('balanceChange', None)
        self.message = data.pop('message', None)
        self.transferTo = data.pop('transferTo', None)
        self.transferFrom = data.pop('transferFrom', None)

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''
        return {
            'id'            : self.id,
            'time'          : self.time,
            'balanceChange' : self.balanceChange,
            'message'       : self.message,
            'transferTo'    : self.transferTo,
            'transferFrom'  : self.transferFrom
        }

class Transaction(object):
    '''
    Class that represents a Transaction object.
    '''

    def __init__(self, data={}):
        '''
        Args:
            data (dict) : transaction fields
        Dictionary keys:
            'amount' (str) Transaction amount
            'currency' (str) Transaction currency as ISO 4217 code. Target
                             wallets must have matching currency.
            'message' (str) Message stored in transaction events.
            'transferTo' (str) ID of another wallet where funds are transferred.
        '''
        self.amount = data.pop('amount', None)
        self.currency = data.pop('currency', None)
        self.message = data.pop('message', None)
        self.transferTo = data.pop('transferTo', None)

    def serialize(self):
        '''
        Return dictionary that is JSON serializable.
        '''
        return {
            'amount'            : self.amount,
            'currency'          : self.currency,
            'message'           : self.message,
            'transferTo'        : self.transferTo
        }
