# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_container.configuration import Configuration


class ContainerBlob(object):
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
        'pulp_href': 'str',
        'pulp_created': 'datetime',
        'artifact': 'str',
        'digest': 'str',
        'media_type': 'str'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'pulp_created': 'pulp_created',
        'artifact': 'artifact',
        'digest': 'digest',
        'media_type': 'media_type'
    }

    def __init__(self, pulp_href=None, pulp_created=None, artifact=None, digest=None, media_type=None, local_vars_configuration=None):  # noqa: E501
        """ContainerBlob - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._pulp_created = None
        self._artifact = None
        self._digest = None
        self._media_type = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        if pulp_created is not None:
            self.pulp_created = pulp_created
        self.artifact = artifact
        self.digest = digest
        self.media_type = media_type

    @property
    def pulp_href(self):
        """Gets the pulp_href of this ContainerBlob.  # noqa: E501


        :return: The pulp_href of this ContainerBlob.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this ContainerBlob.


        :param pulp_href: The pulp_href of this ContainerBlob.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def pulp_created(self):
        """Gets the pulp_created of this ContainerBlob.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this ContainerBlob.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this ContainerBlob.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this ContainerBlob.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def artifact(self):
        """Gets the artifact of this ContainerBlob.  # noqa: E501

        Artifact file representing the physical content  # noqa: E501

        :return: The artifact of this ContainerBlob.  # noqa: E501
        :rtype: str
        """
        return self._artifact

    @artifact.setter
    def artifact(self, artifact):
        """Sets the artifact of this ContainerBlob.

        Artifact file representing the physical content  # noqa: E501

        :param artifact: The artifact of this ContainerBlob.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and artifact is None:  # noqa: E501
            raise ValueError("Invalid value for `artifact`, must not be `None`")  # noqa: E501

        self._artifact = artifact

    @property
    def digest(self):
        """Gets the digest of this ContainerBlob.  # noqa: E501

        sha256 of the Blob file  # noqa: E501

        :return: The digest of this ContainerBlob.  # noqa: E501
        :rtype: str
        """
        return self._digest

    @digest.setter
    def digest(self, digest):
        """Sets the digest of this ContainerBlob.

        sha256 of the Blob file  # noqa: E501

        :param digest: The digest of this ContainerBlob.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and digest is None:  # noqa: E501
            raise ValueError("Invalid value for `digest`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                digest is not None and len(digest) < 1):
            raise ValueError("Invalid value for `digest`, length must be greater than or equal to `1`")  # noqa: E501

        self._digest = digest

    @property
    def media_type(self):
        """Gets the media_type of this ContainerBlob.  # noqa: E501

        Blob media type of the file  # noqa: E501

        :return: The media_type of this ContainerBlob.  # noqa: E501
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        """Sets the media_type of this ContainerBlob.

        Blob media type of the file  # noqa: E501

        :param media_type: The media_type of this ContainerBlob.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and media_type is None:  # noqa: E501
            raise ValueError("Invalid value for `media_type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                media_type is not None and len(media_type) < 1):
            raise ValueError("Invalid value for `media_type`, length must be greater than or equal to `1`")  # noqa: E501

        self._media_type = media_type

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
        if not isinstance(other, ContainerBlob):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ContainerBlob):
            return True

        return self.to_dict() != other.to_dict()
