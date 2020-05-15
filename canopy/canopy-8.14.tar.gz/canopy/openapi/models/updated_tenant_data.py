# coding: utf-8

"""
    Canopy.Api

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from canopy.openapi.configuration import Configuration


class UpdatedTenantData(object):
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
        'name': 'str',
        'short_name': 'str',
        'is_enabled': 'bool',
        'database_id': 'str'
    }

    attribute_map = {
        'name': 'name',
        'short_name': 'shortName',
        'is_enabled': 'isEnabled',
        'database_id': 'databaseId'
    }

    def __init__(self, name=None, short_name=None, is_enabled=None, database_id=None, local_vars_configuration=None):  # noqa: E501
        """UpdatedTenantData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._short_name = None
        self._is_enabled = None
        self._database_id = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if short_name is not None:
            self.short_name = short_name
        if is_enabled is not None:
            self.is_enabled = is_enabled
        if database_id is not None:
            self.database_id = database_id

    @property
    def name(self):
        """Gets the name of this UpdatedTenantData.  # noqa: E501


        :return: The name of this UpdatedTenantData.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdatedTenantData.


        :param name: The name of this UpdatedTenantData.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def short_name(self):
        """Gets the short_name of this UpdatedTenantData.  # noqa: E501


        :return: The short_name of this UpdatedTenantData.  # noqa: E501
        :rtype: str
        """
        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        """Sets the short_name of this UpdatedTenantData.


        :param short_name: The short_name of this UpdatedTenantData.  # noqa: E501
        :type: str
        """

        self._short_name = short_name

    @property
    def is_enabled(self):
        """Gets the is_enabled of this UpdatedTenantData.  # noqa: E501


        :return: The is_enabled of this UpdatedTenantData.  # noqa: E501
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """Sets the is_enabled of this UpdatedTenantData.


        :param is_enabled: The is_enabled of this UpdatedTenantData.  # noqa: E501
        :type: bool
        """

        self._is_enabled = is_enabled

    @property
    def database_id(self):
        """Gets the database_id of this UpdatedTenantData.  # noqa: E501


        :return: The database_id of this UpdatedTenantData.  # noqa: E501
        :rtype: str
        """
        return self._database_id

    @database_id.setter
    def database_id(self, database_id):
        """Sets the database_id of this UpdatedTenantData.


        :param database_id: The database_id of this UpdatedTenantData.  # noqa: E501
        :type: str
        """

        self._database_id = database_id

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
        if not isinstance(other, UpdatedTenantData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdatedTenantData):
            return True

        return self.to_dict() != other.to_dict()
