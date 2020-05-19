from __future__ import absolute_import, unicode_literals, division

import logging
import requests

from paxful.paxful_rest import RestClient
from paxful.trade_client import TradeClient


class PaxfulClient(object):
    url = 'https://paxful.com/api/'

    def __init__(self, api_key='cinow2P4gwP8hCD_MTe6p-YlnhQIeRrtiQswcxx', api_secret='F8Rt6xuKwertRpLVs7vowoDwertX79O_39RK1kLdxx',
                 timeout=None, session=None, logger=None):
        self._rest_client = RestClient(url=self.url,
                                       api_key=api_key,
                                       api_secret=api_secret,
                                       timeout=timeout,
                                       session=session or requests.Session())
        self._logger = logger or logging.getLogger('paxful')

    def _log(self, message):
        """Log a debug message.

        :param message: Debug message.
        :type message: str | unicode
        """
        self._logger.debug(message)

    def offer(self, status=None):
        """
        Return all your offers
        :param status:
        :return: a dict with the number of offers, and the offers themselves
        """
        self._log('Get offer list')
        if status:
            return self._rest_client.post(endpoint='offer/list',
                                          payload={'active': status})
        else:
            return self._rest_client.post(endpoint='offer/list')

    def offer_delete(self, target):
        """
        Delete offer
        :param target: offer hash
        :return:
        """
        return self._rest_client.post(endpoint='offer/delete',
                                      payload={'offer_hash': target})

    def offer_activate(self, target):
        """
        Trun offer on
        :param target: offer hash
        :return:
        """
        return self._rest_client.post(endpoint='offer/activate',
                                      payload={'offer_hash': target})

    def offer_off(self, target: str = None):
        """
        Turns off individual or all offers
        :param target: Individual offer hash
        :return:
        """
        if target:
            return self._rest_client.post(endpoint='offer/deactivate',
                                          payload={'offer_hash': target}
                                          )
        else:
            return self._rest_client.post(endpoint='offer/turn-off')

    def offer_create(self, currency, payment_method, margin, range_min, range_max, tags, req=None,
                     payment_window=30,
                     offer_terms=None,
                     offer_type_field='sell',
                     info: dict = None):
        """
        Create an offer with terms in dict
        :param offer_type_field: 'buy' or 'sell'
        :param currency: 3 letter ISO code for fiat currency. 'USD' or any other. Case insensitive
        :param payment_method: Slug of payment method, for example Western Union needs to be passed as 'western-union'
        :param margin: Float between -99.99 to 21000.00
        :param range_min: Min 1
        :param range_max: Min 1
        :param payment_window: Integer between 30 to 43200 repr minutes
        :param offer_terms: String up to 2500 characters
        :param req: trade requirements str
        :param tags: Comma separated list of tags, if a tag was not approved before, it's ignored	
        :param info: Dict containing other fields no mandatory
        :return:
        """
        requirements = req or "1. Unregistered gift card with: $25, $50, $100 or $200\n2. Receipt (cash or debit)\n3. Picture of card"
        params = {'offer_type_field': offer_type_field,
                  'currency': currency,
                  'payment_method': payment_method,
                  'payment_method_label': 'ATM Always Online',
                  'margin': margin,
                  'range_min': range_min,
                  'range_max': range_max,
                  'payment_window': payment_window,
                  'offer_terms': offer_terms or f'This is an Automated Trading Machine available 24/7. \nVerification of cards is done automatically.\nFollow all instructions and ONLY ENTER WHAT IS ASKED.\n\nRequirements:\n{requirements}\n\nSEE EXAMPLE BELOW\n\nExample Trade:\n*************************************************************************************************\nATM: Hi, thanks for choosing Journey Capital.\nThis is an automated trading platform.\nPlease follow all instructions as they appear.\n\nATM: Please upload receipts.\nYOU: **uploads pictures**\n\nATM: Please upload of card.\nYOU: **uploads pictures**\n\nATM: Please wait while they are verified.....Confirmed!\nATM: Please enter the card number, the expiration date and the CVV (3 pin on back) separated with a comma:\n          Example: 4256125364789531, 07/23, 523\n\nATM: Verifying...please wait\nATM:  4256125364789531 - SUCCESS: $25.0\nATM:  Total given: $25.0\nATM:  Thanks for choosing Journey Capital!\n\nSuccess! Seller has released bitcoins to buyers wallet.\n*************************************************************************************************',
                  'tags': tags,
                  'trade_details': 'Type "HELP" to speak to an actual person.'
                  }
        if info:
            params.update(info)

        return self._rest_client.post(endpoint='offer/create',
                                      payload=params)

    def offer_update(self, target, margin=None, min=None, max=None, tags=None, payment_window=None, currency=None,
                     paymethod=None, offer_details=None):
        """
        Update an offer with info provided in the dict 'info'
        :param target:
        :param currency:
        :param paymethod:
        :param margin:
        :param min:
        :param max:
        :return:
        """
        params = {'offer_hash': target,
                  'currency': currency,
                  'payment_method': paymethod,
                  'payment_method_label': 'ATM Always Online',
                  'margin': margin,
                  'range_min': min,
                  'range_max': max,
                  'payment_window': payment_window,
                  'tags': tags,
                  'offer_terms': offer_details,
                  'trade_details': 'Type "HELP" to speak to an actual person.'
                  }
        info = {}
        for key in params:
            if params[key]:
                info[key] = params[key]
        return self._rest_client.post(endpoint='offer/update',
                                      payload=info)

    def offer_all(self, pay_method, currency):
        """
        Fetch offers from paxful.
        :param pay_method: Payment method slug	, str
        :param currency: Currency code, ex. 'CAD', 'USD'
        :return:
        """
        return self._rest_client.post(endpoint='offer/all',
                                      payload={'offer_type': 'buy',
                                               'payment_method': pay_method,
                                               'currency_code': currency}
                                      )

    def payment_method(self):
        """
        Get list of payment methods
        :return:
        """
        return self._rest_client.post(endpoint='payment-method/list')

    def trade_list(self):
        """List all your active trades

        :return: JSON of all active trade
        """
        self._log('Get list of active trades')
        return self._rest_client.post(endpoint='trade/list')

    def trade(self, hash_id):
        """Creating a trade client for each trade

        :param hash_id: unique identifier for a given trade
        :type: str
        :return Trade client to be used for handling all trade transactions
        :type: TradeClient
        """
        self._log('Create trade object')
        return TradeClient(self._rest_client, hash_id, self._logger)

    def currency_rates(self):
        """List all currencies and their rates (does not require authorization)
        :return: Array of rates data including rates in USD and BTC
        """
        self._log('Get currency rates')
        return self._rest_client.post(endpoint='currency/rates')
