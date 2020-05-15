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


class NamespaceInfoDTO(object):
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
        'meta': 'NamespaceMetaDTO',
        'namespace': 'NamespaceDTO'
    }

    attribute_map = {
        'meta': 'meta',
        'namespace': 'namespace'
    }

    def __init__(self, meta=None, namespace=None, local_vars_configuration=None):  # noqa: E501
        """NamespaceInfoDTO - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._meta = None
        self._namespace = None
        self.discriminator = None

        self.meta = meta
        self.namespace = namespace

    @property
    def meta(self):
        """Gets the meta of this NamespaceInfoDTO.  # noqa: E501


        :return: The meta of this NamespaceInfoDTO.  # noqa: E501
        :rtype: NamespaceMetaDTO
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """Sets the meta of this NamespaceInfoDTO.


        :param meta: The meta of this NamespaceInfoDTO.  # noqa: E501
        :type: NamespaceMetaDTO
        """
        if self.local_vars_configuration.client_side_validation and meta is None:  # noqa: E501
            raise ValueError("Invalid value for `meta`, must not be `None`")  # noqa: E501

        self._meta = meta

    @property
    def namespace(self):
        """Gets the namespace of this NamespaceInfoDTO.  # noqa: E501


        :return: The namespace of this NamespaceInfoDTO.  # noqa: E501
        :rtype: NamespaceDTO
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this NamespaceInfoDTO.


        :param namespace: The namespace of this NamespaceInfoDTO.  # noqa: E501
        :type: NamespaceDTO
        """
        if self.local_vars_configuration.client_side_validation and namespace is None:  # noqa: E501
            raise ValueError("Invalid value for `namespace`, must not be `None`")  # noqa: E501

        self._namespace = namespace

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
        if not isinstance(other, NamespaceInfoDTO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NamespaceInfoDTO):
            return True

        return self.to_dict() != other.to_dict()
