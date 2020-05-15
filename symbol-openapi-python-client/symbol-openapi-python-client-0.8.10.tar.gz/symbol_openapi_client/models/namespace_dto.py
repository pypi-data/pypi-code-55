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


class NamespaceDTO(object):
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
        'registration_type': 'NamespaceRegistrationTypeEnum',
        'depth': 'int',
        'level0': 'str',
        'level1': 'str',
        'level2': 'str',
        'alias': 'AliasDTO',
        'parent_id': 'str',
        'owner_public_key': 'str',
        'owner_address': 'str',
        'start_height': 'str',
        'end_height': 'str'
    }

    attribute_map = {
        'registration_type': 'registrationType',
        'depth': 'depth',
        'level0': 'level0',
        'level1': 'level1',
        'level2': 'level2',
        'alias': 'alias',
        'parent_id': 'parentId',
        'owner_public_key': 'ownerPublicKey',
        'owner_address': 'ownerAddress',
        'start_height': 'startHeight',
        'end_height': 'endHeight'
    }

    def __init__(self, registration_type=None, depth=None, level0=None, level1=None, level2=None, alias=None, parent_id=None, owner_public_key=None, owner_address=None, start_height=None, end_height=None, local_vars_configuration=None):  # noqa: E501
        """NamespaceDTO - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._registration_type = None
        self._depth = None
        self._level0 = None
        self._level1 = None
        self._level2 = None
        self._alias = None
        self._parent_id = None
        self._owner_public_key = None
        self._owner_address = None
        self._start_height = None
        self._end_height = None
        self.discriminator = None

        self.registration_type = registration_type
        self.depth = depth
        self.level0 = level0
        if level1 is not None:
            self.level1 = level1
        if level2 is not None:
            self.level2 = level2
        self.alias = alias
        self.parent_id = parent_id
        self.owner_public_key = owner_public_key
        self.owner_address = owner_address
        self.start_height = start_height
        self.end_height = end_height

    @property
    def registration_type(self):
        """Gets the registration_type of this NamespaceDTO.  # noqa: E501


        :return: The registration_type of this NamespaceDTO.  # noqa: E501
        :rtype: NamespaceRegistrationTypeEnum
        """
        return self._registration_type

    @registration_type.setter
    def registration_type(self, registration_type):
        """Sets the registration_type of this NamespaceDTO.


        :param registration_type: The registration_type of this NamespaceDTO.  # noqa: E501
        :type: NamespaceRegistrationTypeEnum
        """
        if self.local_vars_configuration.client_side_validation and registration_type is None:  # noqa: E501
            raise ValueError("Invalid value for `registration_type`, must not be `None`")  # noqa: E501

        self._registration_type = registration_type

    @property
    def depth(self):
        """Gets the depth of this NamespaceDTO.  # noqa: E501

        Level of the namespace.  # noqa: E501

        :return: The depth of this NamespaceDTO.  # noqa: E501
        :rtype: int
        """
        return self._depth

    @depth.setter
    def depth(self, depth):
        """Sets the depth of this NamespaceDTO.

        Level of the namespace.  # noqa: E501

        :param depth: The depth of this NamespaceDTO.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and depth is None:  # noqa: E501
            raise ValueError("Invalid value for `depth`, must not be `None`")  # noqa: E501

        self._depth = depth

    @property
    def level0(self):
        """Gets the level0 of this NamespaceDTO.  # noqa: E501

        Namespace identifier.  # noqa: E501

        :return: The level0 of this NamespaceDTO.  # noqa: E501
        :rtype: str
        """
        return self._level0

    @level0.setter
    def level0(self, level0):
        """Sets the level0 of this NamespaceDTO.

        Namespace identifier.  # noqa: E501

        :param level0: The level0 of this NamespaceDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and level0 is None:  # noqa: E501
            raise ValueError("Invalid value for `level0`, must not be `None`")  # noqa: E501

        self._level0 = level0

    @property
    def level1(self):
        """Gets the level1 of this NamespaceDTO.  # noqa: E501

        Namespace identifier.  # noqa: E501

        :return: The level1 of this NamespaceDTO.  # noqa: E501
        :rtype: str
        """
        return self._level1

    @level1.setter
    def level1(self, level1):
        """Sets the level1 of this NamespaceDTO.

        Namespace identifier.  # noqa: E501

        :param level1: The level1 of this NamespaceDTO.  # noqa: E501
        :type: str
        """

        self._level1 = level1

    @property
    def level2(self):
        """Gets the level2 of this NamespaceDTO.  # noqa: E501

        Namespace identifier.  # noqa: E501

        :return: The level2 of this NamespaceDTO.  # noqa: E501
        :rtype: str
        """
        return self._level2

    @level2.setter
    def level2(self, level2):
        """Sets the level2 of this NamespaceDTO.

        Namespace identifier.  # noqa: E501

        :param level2: The level2 of this NamespaceDTO.  # noqa: E501
        :type: str
        """

        self._level2 = level2

    @property
    def alias(self):
        """Gets the alias of this NamespaceDTO.  # noqa: E501


        :return: The alias of this NamespaceDTO.  # noqa: E501
        :rtype: AliasDTO
        """
        return self._alias

    @alias.setter
    def alias(self, alias):
        """Sets the alias of this NamespaceDTO.


        :param alias: The alias of this NamespaceDTO.  # noqa: E501
        :type: AliasDTO
        """
        if self.local_vars_configuration.client_side_validation and alias is None:  # noqa: E501
            raise ValueError("Invalid value for `alias`, must not be `None`")  # noqa: E501

        self._alias = alias

    @property
    def parent_id(self):
        """Gets the parent_id of this NamespaceDTO.  # noqa: E501

        Namespace identifier.  # noqa: E501

        :return: The parent_id of this NamespaceDTO.  # noqa: E501
        :rtype: str
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this NamespaceDTO.

        Namespace identifier.  # noqa: E501

        :param parent_id: The parent_id of this NamespaceDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and parent_id is None:  # noqa: E501
            raise ValueError("Invalid value for `parent_id`, must not be `None`")  # noqa: E501

        self._parent_id = parent_id

    @property
    def owner_public_key(self):
        """Gets the owner_public_key of this NamespaceDTO.  # noqa: E501

        Public key.  # noqa: E501

        :return: The owner_public_key of this NamespaceDTO.  # noqa: E501
        :rtype: str
        """
        return self._owner_public_key

    @owner_public_key.setter
    def owner_public_key(self, owner_public_key):
        """Sets the owner_public_key of this NamespaceDTO.

        Public key.  # noqa: E501

        :param owner_public_key: The owner_public_key of this NamespaceDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and owner_public_key is None:  # noqa: E501
            raise ValueError("Invalid value for `owner_public_key`, must not be `None`")  # noqa: E501

        self._owner_public_key = owner_public_key

    @property
    def owner_address(self):
        """Gets the owner_address of this NamespaceDTO.  # noqa: E501

        Address expressed in hexadecimal base.  # noqa: E501

        :return: The owner_address of this NamespaceDTO.  # noqa: E501
        :rtype: str
        """
        return self._owner_address

    @owner_address.setter
    def owner_address(self, owner_address):
        """Sets the owner_address of this NamespaceDTO.

        Address expressed in hexadecimal base.  # noqa: E501

        :param owner_address: The owner_address of this NamespaceDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and owner_address is None:  # noqa: E501
            raise ValueError("Invalid value for `owner_address`, must not be `None`")  # noqa: E501

        self._owner_address = owner_address

    @property
    def start_height(self):
        """Gets the start_height of this NamespaceDTO.  # noqa: E501

        Height of the blockchain.  # noqa: E501

        :return: The start_height of this NamespaceDTO.  # noqa: E501
        :rtype: str
        """
        return self._start_height

    @start_height.setter
    def start_height(self, start_height):
        """Sets the start_height of this NamespaceDTO.

        Height of the blockchain.  # noqa: E501

        :param start_height: The start_height of this NamespaceDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and start_height is None:  # noqa: E501
            raise ValueError("Invalid value for `start_height`, must not be `None`")  # noqa: E501

        self._start_height = start_height

    @property
    def end_height(self):
        """Gets the end_height of this NamespaceDTO.  # noqa: E501

        Height of the blockchain.  # noqa: E501

        :return: The end_height of this NamespaceDTO.  # noqa: E501
        :rtype: str
        """
        return self._end_height

    @end_height.setter
    def end_height(self, end_height):
        """Sets the end_height of this NamespaceDTO.

        Height of the blockchain.  # noqa: E501

        :param end_height: The end_height of this NamespaceDTO.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and end_height is None:  # noqa: E501
            raise ValueError("Invalid value for `end_height`, must not be `None`")  # noqa: E501

        self._end_height = end_height

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
        if not isinstance(other, NamespaceDTO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NamespaceDTO):
            return True

        return self.to_dict() != other.to_dict()
