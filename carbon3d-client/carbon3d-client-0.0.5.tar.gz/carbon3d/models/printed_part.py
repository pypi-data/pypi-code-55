# coding: utf-8

"""
    Carbon DLS API

    Welcome to the Carbon DLS API docs!  A Carbon DLS API token ([JWT](https://en.wikipedia.org/wiki/JSON_Web_Token)) must be included with each request to the API.  Steps to create API tokens: - Create and download an API key [here](https://print.carbon3d.com/api_keys) - For testing: Generate JWT tokens using the [token generator](/token_generator) - For production: Generate JWT tokens dynamically (<em>see authtoken-create.py example</em>) - A valid Carbon API token must be included as <code>Authorization: Bearer [token]</code> HTTP header.  This API provides a programmatic interface for submitting part (and soon build) orders. The general process for creating an order is as follows:  - Upload model files to the API with the [/models](#/Models) endpoint - Create parts that reference a model and a part number with the [/parts](#/Parts) endpoint   -  Part numbers can be created [here](https://print.carbon3d.com/catalog_parts) - Create an order with the [/orders](#/Orders) endpoint  Uploaded models, parts and orders can be retrieved either in bulk or by UUID at the [/models](#/Models), [/parts](#/Parts) and [/orders](#/Orders) endpoints, respectively.  Once a part order is submitted, automatic packing will create one or more builds (for mass-customization applications only).  Builds can be retrieved either in bulk or by UUID at the [/builds](#/Builds) endpoint. - Build attachments (traveler, slice video) can be retrieved by UUID at the [/attachments](#/Attachments) endpoint.  This API also provides a programmatic interface to access [printer](#/Printers) (fleet) status and query for [prints](#/Prints).   # noqa: E501

    The version of the OpenAPI document: 0.0.5
    Contact: api-list@carbon3d.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from carbon3d.configuration import Configuration


class PrintedPart(object):
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
        'uuid': 'str',
        'order_uuid': 'str',
        'part_uuid': 'str',
        'genealogy': 'PartGenealogy',
        'status': 'PrintedPartStatus',
        'serial_number': 'str',
        'build_uuid': 'str',
        'error': 'str'
    }

    attribute_map = {
        'uuid': 'uuid',
        'order_uuid': 'order_uuid',
        'part_uuid': 'part_uuid',
        'genealogy': 'genealogy',
        'status': 'status',
        'serial_number': 'serial_number',
        'build_uuid': 'build_uuid',
        'error': 'error'
    }

    def __init__(self, uuid=None, order_uuid=None, part_uuid=None, genealogy=None, status=None, serial_number=None, build_uuid=None, error=None, local_vars_configuration=None):  # noqa: E501
        """PrintedPart - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._uuid = None
        self._order_uuid = None
        self._part_uuid = None
        self._genealogy = None
        self._status = None
        self._serial_number = None
        self._build_uuid = None
        self._error = None
        self.discriminator = None

        self.uuid = uuid
        self.order_uuid = order_uuid
        self.part_uuid = part_uuid
        self.genealogy = genealogy
        self.status = status
        if serial_number is not None:
            self.serial_number = serial_number
        if build_uuid is not None:
            self.build_uuid = build_uuid
        if error is not None:
            self.error = error

    @property
    def uuid(self):
        """Gets the uuid of this PrintedPart.  # noqa: E501

        Printed Part UUID  # noqa: E501

        :return: The uuid of this PrintedPart.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this PrintedPart.

        Printed Part UUID  # noqa: E501

        :param uuid: The uuid of this PrintedPart.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and uuid is None:  # noqa: E501
            raise ValueError("Invalid value for `uuid`, must not be `None`")  # noqa: E501

        self._uuid = uuid

    @property
    def order_uuid(self):
        """Gets the order_uuid of this PrintedPart.  # noqa: E501

        Order UUID  # noqa: E501

        :return: The order_uuid of this PrintedPart.  # noqa: E501
        :rtype: str
        """
        return self._order_uuid

    @order_uuid.setter
    def order_uuid(self, order_uuid):
        """Sets the order_uuid of this PrintedPart.

        Order UUID  # noqa: E501

        :param order_uuid: The order_uuid of this PrintedPart.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and order_uuid is None:  # noqa: E501
            raise ValueError("Invalid value for `order_uuid`, must not be `None`")  # noqa: E501

        self._order_uuid = order_uuid

    @property
    def part_uuid(self):
        """Gets the part_uuid of this PrintedPart.  # noqa: E501

        Part UUID  # noqa: E501

        :return: The part_uuid of this PrintedPart.  # noqa: E501
        :rtype: str
        """
        return self._part_uuid

    @part_uuid.setter
    def part_uuid(self, part_uuid):
        """Sets the part_uuid of this PrintedPart.

        Part UUID  # noqa: E501

        :param part_uuid: The part_uuid of this PrintedPart.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and part_uuid is None:  # noqa: E501
            raise ValueError("Invalid value for `part_uuid`, must not be `None`")  # noqa: E501

        self._part_uuid = part_uuid

    @property
    def genealogy(self):
        """Gets the genealogy of this PrintedPart.  # noqa: E501


        :return: The genealogy of this PrintedPart.  # noqa: E501
        :rtype: PartGenealogy
        """
        return self._genealogy

    @genealogy.setter
    def genealogy(self, genealogy):
        """Sets the genealogy of this PrintedPart.


        :param genealogy: The genealogy of this PrintedPart.  # noqa: E501
        :type: PartGenealogy
        """

        self._genealogy = genealogy

    @property
    def status(self):
        """Gets the status of this PrintedPart.  # noqa: E501


        :return: The status of this PrintedPart.  # noqa: E501
        :rtype: PrintedPartStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this PrintedPart.


        :param status: The status of this PrintedPart.  # noqa: E501
        :type: PrintedPartStatus
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def serial_number(self):
        """Gets the serial_number of this PrintedPart.  # noqa: E501

        Serial Number (after printing)  # noqa: E501

        :return: The serial_number of this PrintedPart.  # noqa: E501
        :rtype: str
        """
        return self._serial_number

    @serial_number.setter
    def serial_number(self, serial_number):
        """Sets the serial_number of this PrintedPart.

        Serial Number (after printing)  # noqa: E501

        :param serial_number: The serial_number of this PrintedPart.  # noqa: E501
        :type: str
        """

        self._serial_number = serial_number

    @property
    def build_uuid(self):
        """Gets the build_uuid of this PrintedPart.  # noqa: E501

        Build UUID  # noqa: E501

        :return: The build_uuid of this PrintedPart.  # noqa: E501
        :rtype: str
        """
        return self._build_uuid

    @build_uuid.setter
    def build_uuid(self, build_uuid):
        """Sets the build_uuid of this PrintedPart.

        Build UUID  # noqa: E501

        :param build_uuid: The build_uuid of this PrintedPart.  # noqa: E501
        :type: str
        """

        self._build_uuid = build_uuid

    @property
    def error(self):
        """Gets the error of this PrintedPart.  # noqa: E501

        Error message (if part could not be produced)  # noqa: E501

        :return: The error of this PrintedPart.  # noqa: E501
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this PrintedPart.

        Error message (if part could not be produced)  # noqa: E501

        :param error: The error of this PrintedPart.  # noqa: E501
        :type: str
        """

        self._error = error

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
        if not isinstance(other, PrintedPart):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PrintedPart):
            return True

        return self.to_dict() != other.to_dict()
