from __future__ import absolute_import, unicode_literals, division

import datetime


class TradeClient(object):

    def __init__(self, rest_client, hash_id, logger, card_count=None, codes=None, status=None):
        """Initialize trade object , each object will be a single trade

        :param rest_client: from global Rest Client
        :param hash_id: Hash ID of a trade
        :param logger: Logger to record debug messages with
        """
        self._rest_client = rest_client
        self._logger = logger
        self._hash = hash_id
        self.card_count = card_count
        self.codes = codes
        self.status = status
        self.fiat_given = 0.00
        self.deposit_request = 0.00
        self.deposit = 0.00
        self.crypto_currency = ''
        self.market_price = 0.00
        self.tsx_id = ''
        self.time = datetime.datetime.utcnow()
        self.attempt = 3
        self.attachments = []
        self.info()
        self.country = ''

    def _log(self, message):
        """Log a debug message.

        :param message: Debug message.
        :type message: str | unicode
        """
        self._logger.debug(message)

    def get_hash(self):

        return self._hash

    def info(self):

        self._log("Get trade info")

        resp = self._rest_client.post(
            endpoint='trade/get',
            payload={'trade_hash': self._hash}
        )

        self.fiat_requested = float(resp['data']['trade']['fiat_amount_requested'])
        self.usdrate = resp['data']['trade']['crypto_current_rate_usd']
        self.status = resp['data']['trade']['trade_status']
        self.crypto_requested = resp['data']['trade']['crypto_amount_requested']
        self.crypto_total = resp['data']['trade']['crypto_amount_total']
        self.offer = resp['data']['trade']['offer_hash']
        self.currency = resp['data']['trade']['fiat_currency_code']

        # all info in dict
        self.all_info = resp['data']['trade']

    def get_chat(self):

        self._log(f"{self._hash} - Get chat messages")

        return self._rest_client.post(
            endpoint='trade-chat/get',
            payload={'trade_hash': self._hash}
        )

    def get_image(self, image_hash: str):

        self._log(f"{self._hash} - Fetching image")

        return self._rest_client.post(
            endpoint='trade-chat/image',
            payload={'image_hash': image_hash}
        )

    def post_chat(self, message):

        self._log(f"{self._hash} - Sent to chat -> {message}")

        return self._rest_client.post(
            endpoint='trade-chat/post',
            payload={'trade_hash': self._hash, 'message': message}
        )

    def release(self):
        """
        Release bitcoins for a trade
        :return: Boolean on successful release
        """
        return self._rest_client.post(
            endpoint='trade/release',
            payload={'trade_hash': self._hash}
        )

    def feedback(self):
        """
        Gives good feedback
        :return:
        """
        return self._rest_client.post(
            endpoint='feedback/give',
            payload={'trade_hash': self._hash, 'message': 'Great! Thanks for choosing _________', 'rating': 1}
        )

    def dispute(self, reason):
        """
        Open dispute for a trade with reason

        :param reason: String describing dispute
        :return: Boolean of successful start of dispute
        """
        return self._rest_client.post(
            endpoint='trade/dispute',
            payload={'trade_hash': self._hash, 'reason': reason}
        )

