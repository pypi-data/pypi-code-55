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
import datetime

import symbol_openapi_client
from symbol_openapi_client.models.namespace_metadata_transaction_body_dto import NamespaceMetadataTransactionBodyDTO  # noqa: E501
from symbol_openapi_client.rest import ApiException

class TestNamespaceMetadataTransactionBodyDTO(unittest.TestCase):
    """NamespaceMetadataTransactionBodyDTO unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test NamespaceMetadataTransactionBodyDTO
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = symbol_openapi_client.models.namespace_metadata_transaction_body_dto.NamespaceMetadataTransactionBodyDTO()  # noqa: E501
        if include_optional :
            return NamespaceMetadataTransactionBodyDTO(
                target_public_key = 'AC1A6E1D8DE5B17D2C6B1293F1CAD3829EEACF38D09311BB3C8E5A880092DE26', 
                scoped_metadata_key = '0DC67FBE1CAD29E3', 
                target_namespace_id = '85BBEA6CC462B244', 
                value_size_delta = 56, 
                value_size = 56, 
                value = '0'
            )
        else :
            return NamespaceMetadataTransactionBodyDTO(
                target_public_key = 'AC1A6E1D8DE5B17D2C6B1293F1CAD3829EEACF38D09311BB3C8E5A880092DE26',
                scoped_metadata_key = '0DC67FBE1CAD29E3',
                value_size_delta = 56,
                value_size = 56,
                value = '0',
        )

    def testNamespaceMetadataTransactionBodyDTO(self):
        """Test NamespaceMetadataTransactionBodyDTO"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
