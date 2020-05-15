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


import pprint
import re  # noqa: F401

import six

from symbol_openapi_client.configuration import Configuration


class BalanceTransferReceiptDTO(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'version': 'int',
        'type': 'ReceiptTypeEnum',
        'mosaic_id': 'str',
        'amount': 'str',
        'sender_public_key': 'str',
        'recipient_address': 'str'
    }

    attribute_map = {
        'version': 'version',
        'type': 'type',
        'mosaic_id': 'mosaicId',
        'amount': 'amount',
        'sender_public_key': 'senderPublicKey',
        'recipient_address': 'recipientAddress'
    }

    def __init__(self, version=None, type=None, mosaic_id=None, amount=None, sender_public_key=None, recipient_address=None, local_vars_configuration=None):  # noqa: E501
        """BalanceTransferReceiptDTO - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._version = None
        self._type = None
        self._mosaic_id = None
        self._amount = None
        self._sender_public_key = None
        self._recipient_address = None
        self.discriminator = None

        self.version = version
        self.type = type
        self.mosaic_id = mosaic_id
        self.amount = amount
        self.sender_public_key = sender_public_key
        self.recipient_address = recipient_address

    @property
    def version(self):
        """Gets the version of this BalanceTransferReceiptDTO.  # noqa: E501

        Version of the receipt.  # noqa: E501

        :return: The version of this BalanceTransferReceiptDTO.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this BalanceTransferReceiptDTO.

        Version of the receipt.  # noqa: E501

        :param version: The version of this BalanceTransferReceiptDTO.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def type(self):
        """Gets the type of this BalanceTransferReceiptDTO.  # noqa: E501


        :return: The type of this BalanceTransferReceiptDTO.  # noqa: E501
        :rtype: ReceiptTypeEnum
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this BalanceTransferReceiptDTO.


        :param type: The type of this BalanceTransferReceiptDTO.  # noqa: E501
        :type: ReceiptTypeEnum
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def mosaic_id(self):
        """Gets the mosaic_id of this BalanceTransferReceiptDTO.  # noqa: E501

        Mosaic identifier.  # noqa: E501

        :return: The mosaic_id of this BalanceTransferReceiptDTO.  # noqa: E501
        :rtype: str
        """
        return self._mosaic_id

    @mosaic_id.setter
    def mosaic_id(self, mosaic_id):
        """Sets the mosaic_id of this BalanceTransferReceiptDTO.

        Mosaic identifier.  # noqa: E501

        :param mosaic_id: The mosaic_id of this BalanceTransferReceiptDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and mosaic_id is None:  # noqa: E501
            raise ValueError("Invalid value for `mosaic_id`, must not be `None`")  # noqa: E501

        self._mosaic_id = mosaic_id

    @property
    def amount(self):
        """Gets the amount of this BalanceTransferReceiptDTO.  # noqa: E501

        Absolute amount. An amount of 123456789 (absolute) for a mosaic with divisibility 6 means 123.456789 (relative).  # noqa: E501

        :return: The amount of this BalanceTransferReceiptDTO.  # noqa: E501
        :rtype: str
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this BalanceTransferReceiptDTO.

        Absolute amount. An amount of 123456789 (absolute) for a mosaic with divisibility 6 means 123.456789 (relative).  # noqa: E501

        :param amount: The amount of this BalanceTransferReceiptDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and amount is None:  # noqa: E501
            raise ValueError("Invalid value for `amount`, must not be `None`")  # noqa: E501

        self._amount = amount

    @property
    def sender_public_key(self):
        """Gets the sender_public_key of this BalanceTransferReceiptDTO.  # noqa: E501

        Public key.  # noqa: E501

        :return: The sender_public_key of this BalanceTransferReceiptDTO.  # noqa: E501
        :rtype: str
        """
        return self._sender_public_key

    @sender_public_key.setter
    def sender_public_key(self, sender_public_key):
        """Sets the sender_public_key of this BalanceTransferReceiptDTO.

        Public key.  # noqa: E501

        :param sender_public_key: The sender_public_key of this BalanceTransferReceiptDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and sender_public_key is None:  # noqa: E501
            raise ValueError("Invalid value for `sender_public_key`, must not be `None`")  # noqa: E501

        self._sender_public_key = sender_public_key

    @property
    def recipient_address(self):
        """Gets the recipient_address of this BalanceTransferReceiptDTO.  # noqa: E501

        Address expressed in hexadecimal base.  # noqa: E501

        :return: The recipient_address of this BalanceTransferReceiptDTO.  # noqa: E501
        :rtype: str
        """
        return self._recipient_address

    @recipient_address.setter
    def recipient_address(self, recipient_address):
        """Sets the recipient_address of this BalanceTransferReceiptDTO.

        Address expressed in hexadecimal base.  # noqa: E501

        :param recipient_address: The recipient_address of this BalanceTransferReceiptDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and recipient_address is None:  # noqa: E501
            raise ValueError("Invalid value for `recipient_address`, must not be `None`")  # noqa: E501

        self._recipient_address = recipient_address

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BalanceTransferReceiptDTO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BalanceTransferReceiptDTO):
            return True

        return self.to_dict() != other.to_dict()
