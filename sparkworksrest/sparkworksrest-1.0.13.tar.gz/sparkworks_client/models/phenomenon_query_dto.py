# coding: utf-8

"""
    SparkWorks Core API

    Management Service for the SparkWorks Processing Engine  # noqa: E501

    OpenAPI spec version: v2.0
    Contact: info@sparkworks.net
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class PhenomenonQueryDTO(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'uuid': 'str'
    }

    attribute_map = {
        'name': 'name',
        'uuid': 'uuid'
    }

    def __init__(self, name=None, uuid=None):  # noqa: E501
        """PhenomenonQueryDTO - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._uuid = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if uuid is not None:
            self.uuid = uuid

    @property
    def name(self):
        """Gets the name of this PhenomenonQueryDTO.  # noqa: E501


        :return: The name of this PhenomenonQueryDTO.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PhenomenonQueryDTO.


        :param name: The name of this PhenomenonQueryDTO.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def uuid(self):
        """Gets the uuid of this PhenomenonQueryDTO.  # noqa: E501


        :return: The uuid of this PhenomenonQueryDTO.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this PhenomenonQueryDTO.


        :param uuid: The uuid of this PhenomenonQueryDTO.  # noqa: E501
        :type: str
        """

        self._uuid = uuid

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(PhenomenonQueryDTO, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PhenomenonQueryDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
