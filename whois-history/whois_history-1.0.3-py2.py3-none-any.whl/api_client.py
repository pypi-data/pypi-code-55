# -*- coding: utf-8 -*-
from typing import List
from datetime import date
import json
from .exceptions import UnparsableResponseException, EmptyResponseException
from .requester import Requester

from .models.historic import WhoisRecord, ErrorMessage

__version__ = '1.0.3'


class ApiClient:
    __version = __version__
    __url_whois = "https://whois-history.whoisxmlapi.com/api/v1"
    __user_agent = "whoishistory-python/" + __version__

    def __init__(self, api_key):
        """Init ApiClient instance.
            :param api_key: your api_key
        """

        self.api_key = api_key

        self.requester = Requester(self.__user_agent)

    def purchase(self, domain_name: str, **options) -> List[WhoisRecord]:
        """Purchase returns the slice of records.

            :param domain_name: the domain for which historic WHOIS data is requested
            :key sinceDate: search records discovered since the given date
            :key createdDateFrom: search records created after given date
            :key createdDateTo: search records created before given date
            :key updatedDateFrom: search records updated after given date
            :key updatedDateTo: search records updated before given date
            :key expiredDateFrom: search records expires after given date
            :key expiredDateTo: search records expires before given date
        """

        parsed = self.__call_api(self.__url_whois, method='GET', params={
            'domainName': domain_name,
            'apiKey': self.api_key,
            'outputFormat': 'JSON',
            'mode': 'purchase',
        }, **options)

        if 'records' not in parsed:
            raise EmptyResponseException()

        res: List[WhoisRecord] = list()

        records = parsed['records']
        if isinstance(records, list):
            for r in records:
                res.append(WhoisRecord(r))

        return res

    def preview(self, domain_name: str, **options: date) -> int:
        """Preview returns the number of records. No credits deducted.

            :param domain_name: the domain for which historic WHOIS data is requested
            :key sinceDate: search records discovered since the given date
            :key createdDateFrom: search records created after given date
            :key createdDateTo: search records created before given date
            :key updatedDateFrom: search records updated after given date
            :key updatedDateTo: search records updated before given date
            :key expiredDateFrom: search records expires after given date
            :key expiredDateTo: search records expires before given date
        """

        parsed = self.__call_api(self.__url_whois, method='GET', params={
            'domainName': domain_name,
            'apiKey': self.api_key,
            'outputFormat': 'JSON',
            'mode': 'preview',
        }, **options)

        if 'recordsCount' not in parsed:
            raise EmptyResponseException()

        return int(parsed['recordsCount'])

    __options = [
        'sinceDate',
        'createdDateFrom',
        'createdDateTo',
        'updatedDateFrom',
        'updatedDateTo',
        'expiredDateFrom',
        'expiredDateTo',
    ]

    def __call_api(self, url, method, headers: dict = None, params: dict = None, **options) -> dict:

        if params is None:
            params = dict()

        for k in options:
            if k in self.__options:
                d: date = options[k]
                params[k] = d.strftime("%Y-%m-%d")

        response = self.requester.request(url, method=method, headers=headers, params=params)

        text = response.text

        if len(text) == 0:
            raise EmptyResponseException()

        parsed = self.__parse(text)

        if 'code' in parsed or 'messages' in parsed:
            raise ErrorMessage(parsed)

        return parsed

    @staticmethod
    def __parse(string_response) -> dict:
        try:
            dictionary = json.loads(string_response)
        except Exception as e:
            raise UnparsableResponseException(e.__str__())

        return dictionary

    def set_requester(self, requester):
        """Set the requester instance.

            Keyword arguments:
            :param requester: the Requester instance
        """

        if isinstance(requester, Requester):
            self.requester = requester
