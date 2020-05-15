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


class RentalFeesDTO(object):
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
        'effective_root_namespace_rental_fee_per_block': 'str',
        'effective_child_namespace_rental_fee': 'str',
        'effective_mosaic_rental_fee': 'str'
    }

    attribute_map = {
        'effective_root_namespace_rental_fee_per_block': 'effectiveRootNamespaceRentalFeePerBlock',
        'effective_child_namespace_rental_fee': 'effectiveChildNamespaceRentalFee',
        'effective_mosaic_rental_fee': 'effectiveMosaicRentalFee'
    }

    def __init__(self, effective_root_namespace_rental_fee_per_block=None, effective_child_namespace_rental_fee=None, effective_mosaic_rental_fee=None, local_vars_configuration=None):  # noqa: E501
        """RentalFeesDTO - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._effective_root_namespace_rental_fee_per_block = None
        self._effective_child_namespace_rental_fee = None
        self._effective_mosaic_rental_fee = None
        self.discriminator = None

        self.effective_root_namespace_rental_fee_per_block = effective_root_namespace_rental_fee_per_block
        self.effective_child_namespace_rental_fee = effective_child_namespace_rental_fee
        self.effective_mosaic_rental_fee = effective_mosaic_rental_fee

    @property
    def effective_root_namespace_rental_fee_per_block(self):
        """Gets the effective_root_namespace_rental_fee_per_block of this RentalFeesDTO.  # noqa: E501

        Absolute amount. An amount of 123456789 (absolute) for a mosaic with divisibility 6 means 123.456789 (relative).  # noqa: E501

        :return: The effective_root_namespace_rental_fee_per_block of this RentalFeesDTO.  # noqa: E501
        :rtype: str
        """
        return self._effective_root_namespace_rental_fee_per_block

    @effective_root_namespace_rental_fee_per_block.setter
    def effective_root_namespace_rental_fee_per_block(self, effective_root_namespace_rental_fee_per_block):
        """Sets the effective_root_namespace_rental_fee_per_block of this RentalFeesDTO.

        Absolute amount. An amount of 123456789 (absolute) for a mosaic with divisibility 6 means 123.456789 (relative).  # noqa: E501

        :param effective_root_namespace_rental_fee_per_block: The effective_root_namespace_rental_fee_per_block of this RentalFeesDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and effective_root_namespace_rental_fee_per_block is None:  # noqa: E501
            raise ValueError("Invalid value for `effective_root_namespace_rental_fee_per_block`, must not be `None`")  # noqa: E501

        self._effective_root_namespace_rental_fee_per_block = effective_root_namespace_rental_fee_per_block

    @property
    def effective_child_namespace_rental_fee(self):
        """Gets the effective_child_namespace_rental_fee of this RentalFeesDTO.  # noqa: E501

        Absolute amount. An amount of 123456789 (absolute) for a mosaic with divisibility 6 means 123.456789 (relative).  # noqa: E501

        :return: The effective_child_namespace_rental_fee of this RentalFeesDTO.  # noqa: E501
        :rtype: str
        """
        return self._effective_child_namespace_rental_fee

    @effective_child_namespace_rental_fee.setter
    def effective_child_namespace_rental_fee(self, effective_child_namespace_rental_fee):
        """Sets the effective_child_namespace_rental_fee of this RentalFeesDTO.

        Absolute amount. An amount of 123456789 (absolute) for a mosaic with divisibility 6 means 123.456789 (relative).  # noqa: E501

        :param effective_child_namespace_rental_fee: The effective_child_namespace_rental_fee of this RentalFeesDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and effective_child_namespace_rental_fee is None:  # noqa: E501
            raise ValueError("Invalid value for `effective_child_namespace_rental_fee`, must not be `None`")  # noqa: E501

        self._effective_child_namespace_rental_fee = effective_child_namespace_rental_fee

    @property
    def effective_mosaic_rental_fee(self):
        """Gets the effective_mosaic_rental_fee of this RentalFeesDTO.  # noqa: E501

        Absolute amount. An amount of 123456789 (absolute) for a mosaic with divisibility 6 means 123.456789 (relative).  # noqa: E501

        :return: The effective_mosaic_rental_fee of this RentalFeesDTO.  # noqa: E501
        :rtype: str
        """
        return self._effective_mosaic_rental_fee

    @effective_mosaic_rental_fee.setter
    def effective_mosaic_rental_fee(self, effective_mosaic_rental_fee):
        """Sets the effective_mosaic_rental_fee of this RentalFeesDTO.

        Absolute amount. An amount of 123456789 (absolute) for a mosaic with divisibility 6 means 123.456789 (relative).  # noqa: E501

        :param effective_mosaic_rental_fee: The effective_mosaic_rental_fee of this RentalFeesDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and effective_mosaic_rental_fee is None:  # noqa: E501
            raise ValueError("Invalid value for `effective_mosaic_rental_fee`, must not be `None`")  # noqa: E501

        self._effective_mosaic_rental_fee = effective_mosaic_rental_fee

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
        if not isinstance(other, RentalFeesDTO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RentalFeesDTO):
            return True

        return self.to_dict() != other.to_dict()
