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

from sparkworks_client.models.single_resource_measurement_api_model import SingleResourceMeasurementAPIModel  # noqa: F401,E501


class QueryRawDataTimeRangeResultDTOAPIModel(object):
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
        '_from': 'int',
        'phenomenon_uuid': 'str',
        'resource_uuid': 'str',
        'results': 'list[SingleResourceMeasurementAPIModel]',
        'to': 'int',
        'unit_uuid': 'str'
    }

    attribute_map = {
        '_from': 'from',
        'phenomenon_uuid': 'phenomenonUuid',
        'resource_uuid': 'resourceUuid',
        'results': 'results',
        'to': 'to',
        'unit_uuid': 'unitUuid'
    }

    def __init__(self, _from=None, phenomenon_uuid=None, resource_uuid=None, results=None, to=None, unit_uuid=None):  # noqa: E501
        """QueryRawDataTimeRangeResultDTOAPIModel - a model defined in Swagger"""  # noqa: E501

        self.__from = None
        self._phenomenon_uuid = None
        self._resource_uuid = None
        self._results = None
        self._to = None
        self._unit_uuid = None
        self.discriminator = None

        self._from = _from
        if phenomenon_uuid is not None:
            self.phenomenon_uuid = phenomenon_uuid
        if resource_uuid is not None:
            self.resource_uuid = resource_uuid
        if results is not None:
            self.results = results
        self.to = to
        if unit_uuid is not None:
            self.unit_uuid = unit_uuid

    @property
    def _from(self):
        """Gets the _from of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501

        The UNIX timestamp of the start date for filtering  # noqa: E501

        :return: The _from of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :rtype: int
        """
        return self.__from

    @_from.setter
    def _from(self, _from):
        """Sets the _from of this QueryRawDataTimeRangeResultDTOAPIModel.

        The UNIX timestamp of the start date for filtering  # noqa: E501

        :param _from: The _from of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :type: int
        """
        if _from is None:
            raise ValueError("Invalid value for `_from`, must not be `None`")  # noqa: E501

        self.__from = _from

    @property
    def phenomenon_uuid(self):
        """Gets the phenomenon_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501

        The Resource's Phenomenon UUID  # noqa: E501

        :return: The phenomenon_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :rtype: str
        """
        return self._phenomenon_uuid

    @phenomenon_uuid.setter
    def phenomenon_uuid(self, phenomenon_uuid):
        """Sets the phenomenon_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.

        The Resource's Phenomenon UUID  # noqa: E501

        :param phenomenon_uuid: The phenomenon_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :type: str
        """

        self._phenomenon_uuid = phenomenon_uuid

    @property
    def resource_uuid(self):
        """Gets the resource_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501

        The UUID of the Resource  # noqa: E501

        :return: The resource_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :rtype: str
        """
        return self._resource_uuid

    @resource_uuid.setter
    def resource_uuid(self, resource_uuid):
        """Sets the resource_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.

        The UUID of the Resource  # noqa: E501

        :param resource_uuid: The resource_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :type: str
        """

        self._resource_uuid = resource_uuid

    @property
    def results(self):
        """Gets the results of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501

        The requested raw data  # noqa: E501

        :return: The results of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :rtype: list[SingleResourceMeasurementAPIModel]
        """
        return self._results

    @results.setter
    def results(self, results):
        """Sets the results of this QueryRawDataTimeRangeResultDTOAPIModel.

        The requested raw data  # noqa: E501

        :param results: The results of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :type: list[SingleResourceMeasurementAPIModel]
        """

        self._results = results

    @property
    def to(self):
        """Gets the to of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501

        The UNIX timestamp of the end date for filtering  # noqa: E501

        :return: The to of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :rtype: int
        """
        return self._to

    @to.setter
    def to(self, to):
        """Sets the to of this QueryRawDataTimeRangeResultDTOAPIModel.

        The UNIX timestamp of the end date for filtering  # noqa: E501

        :param to: The to of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :type: int
        """
        if to is None:
            raise ValueError("Invalid value for `to`, must not be `None`")  # noqa: E501

        self._to = to

    @property
    def unit_uuid(self):
        """Gets the unit_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501

        The Resource's Unit UUID  # noqa: E501

        :return: The unit_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :rtype: str
        """
        return self._unit_uuid

    @unit_uuid.setter
    def unit_uuid(self, unit_uuid):
        """Sets the unit_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.

        The Resource's Unit UUID  # noqa: E501

        :param unit_uuid: The unit_uuid of this QueryRawDataTimeRangeResultDTOAPIModel.  # noqa: E501
        :type: str
        """

        self._unit_uuid = unit_uuid

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
        if issubclass(QueryRawDataTimeRangeResultDTOAPIModel, dict):
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
        if not isinstance(other, QueryRawDataTimeRangeResultDTOAPIModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
