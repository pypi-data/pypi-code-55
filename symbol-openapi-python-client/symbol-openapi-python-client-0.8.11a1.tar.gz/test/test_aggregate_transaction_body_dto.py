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
from symbol_openapi_client.models.aggregate_transaction_body_dto import AggregateTransactionBodyDTO  # noqa: E501
from symbol_openapi_client.rest import ApiException

class TestAggregateTransactionBodyDTO(unittest.TestCase):
    """AggregateTransactionBodyDTO unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AggregateTransactionBodyDTO
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = symbol_openapi_client.models.aggregate_transaction_body_dto.AggregateTransactionBodyDTO()  # noqa: E501
        if include_optional :
            return AggregateTransactionBodyDTO(
                transactions_hash = 'C8FC3FB54FDDFBCE0E8C71224990124E4EEC5AD5D30E592EDFA9524669A23810', 
                cosignatures = [
                    symbol_openapi_client.models.cosignature_dto.CosignatureDTO()
                    ], 
                transactions = [
                    symbol_openapi_client.models.embedded_transaction_info_dto.EmbeddedTransactionInfoDTO(
                        meta = symbol_openapi_client.models.embedded_transaction_meta_dto.EmbeddedTransactionMetaDTO(
                            height = '1', 
                            aggregate_hash = 'C8FC3FB54FDDFBCE0E8C71224990124E4EEC5AD5D30E592EDFA9524669A23810', 
                            aggregate_id = '0', 
                            index = 56, 
                            id = '0', ), 
                        transaction = null, )
                    ]
            )
        else :
            return AggregateTransactionBodyDTO(
                transactions_hash = 'C8FC3FB54FDDFBCE0E8C71224990124E4EEC5AD5D30E592EDFA9524669A23810',
                cosignatures = [
                    symbol_openapi_client.models.cosignature_dto.CosignatureDTO()
                    ],
                transactions = [
                    symbol_openapi_client.models.embedded_transaction_info_dto.EmbeddedTransactionInfoDTO(
                        meta = symbol_openapi_client.models.embedded_transaction_meta_dto.EmbeddedTransactionMetaDTO(
                            height = '1', 
                            aggregate_hash = 'C8FC3FB54FDDFBCE0E8C71224990124E4EEC5AD5D30E592EDFA9524669A23810', 
                            aggregate_id = '0', 
                            index = 56, 
                            id = '0', ), 
                        transaction = null, )
                    ],
        )

    def testAggregateTransactionBodyDTO(self):
        """Test AggregateTransactionBodyDTO"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
