# coding: utf-8

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

import unittest

import symbol_openapi_client
from symbol_openapi_client.api.chain_routes_api import ChainRoutesApi  # noqa: E501
from symbol_openapi_client.rest import ApiException


class TestChainRoutesApi(unittest.TestCase):
    """ChainRoutesApi unit test stubs"""

    def setUp(self):
        self.api = symbol_openapi_client.api.chain_routes_api.ChainRoutesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_chain_height(self):
        """Test case for get_chain_height

        Get the current height of the chain  # noqa: E501
        """
        pass

    def test_get_chain_score(self):
        """Test case for get_chain_score

        Get the current score of the chain  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
