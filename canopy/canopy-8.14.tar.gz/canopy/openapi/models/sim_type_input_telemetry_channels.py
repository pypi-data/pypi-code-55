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


class SimTypeInputTelemetryChannels(object):
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
        'valid_source_sim_types': 'list[str]',
        'channels': 'list[SimTypeInputTelemetryChannel]'
    }

    attribute_map = {
        'valid_source_sim_types': 'validSourceSimTypes',
        'channels': 'channels'
    }

    def __init__(self, valid_source_sim_types=None, channels=None, local_vars_configuration=None):  # noqa: E501
        """SimTypeInputTelemetryChannels - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._valid_source_sim_types = None
        self._channels = None
        self.discriminator = None

        if valid_source_sim_types is not None:
            self.valid_source_sim_types = valid_source_sim_types
        if channels is not None:
            self.channels = channels

    @property
    def valid_source_sim_types(self):
        """Gets the valid_source_sim_types of this SimTypeInputTelemetryChannels.  # noqa: E501


        :return: The valid_source_sim_types of this SimTypeInputTelemetryChannels.  # noqa: E501
        :rtype: list[str]
        """
        return self._valid_source_sim_types

    @valid_source_sim_types.setter
    def valid_source_sim_types(self, valid_source_sim_types):
        """Sets the valid_source_sim_types of this SimTypeInputTelemetryChannels.


        :param valid_source_sim_types: The valid_source_sim_types of this SimTypeInputTelemetryChannels.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["StraightSim", "ApexSim", "QuasiStaticLap", "GenerateRacingLine", "DeploymentLap", "FailureSim", "SuccessSim", "Virtual4Post", "LimitSim", "DriveCycleSim", "DynamicLap", "DragSim", "DynamicMultiLap", "ThermalReplay", "TyreReplay", "PacejkaCanopyConverter", "AircraftSim", "ChannelInference", "Telemetry", "OvertakingLap", "TyreThermalDynamicLap", "TyreThermalDynamicMultiLap", "DynamicLapWithSLS", "DynamicLapHD", "IliadCollocation", "SubLimitSim", "ConstraintSatisfier"]  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                not set(valid_source_sim_types).issubset(set(allowed_values))):  # noqa: E501
            raise ValueError(
                "Invalid values for `valid_source_sim_types` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(valid_source_sim_types) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._valid_source_sim_types = valid_source_sim_types

    @property
    def channels(self):
        """Gets the channels of this SimTypeInputTelemetryChannels.  # noqa: E501


        :return: The channels of this SimTypeInputTelemetryChannels.  # noqa: E501
        :rtype: list[SimTypeInputTelemetryChannel]
        """
        return self._channels

    @channels.setter
    def channels(self, channels):
        """Sets the channels of this SimTypeInputTelemetryChannels.


        :param channels: The channels of this SimTypeInputTelemetryChannels.  # noqa: E501
        :type: list[SimTypeInputTelemetryChannel]
        """

        self._channels = channels

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
        if not isinstance(other, SimTypeInputTelemetryChannels):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SimTypeInputTelemetryChannels):
            return True

        return self.to_dict() != other.to_dict()
