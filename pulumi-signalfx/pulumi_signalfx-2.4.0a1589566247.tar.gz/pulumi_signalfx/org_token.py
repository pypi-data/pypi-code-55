# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class OrgToken(pulumi.CustomResource):
    description: pulumi.Output[str]
    """
    Description of the token.
    """
    disabled: pulumi.Output[bool]
    """
    Flag that controls enabling the token. If set to `true`, the token is disabled, and you can't use it for authentication. Defaults to `false`.
    """
    dpm_limits: pulumi.Output[dict]
    """
    Specify DPM-based limits for this token.

      * `dpmLimit` (`float`) - The datapoints per minute (dpm) limit for this token. If you exceed this limit, SignalFx sends out an alert.
      * `dpmNotificationThreshold` (`float`) - DPM level at which SignalFx sends the notification for this token. If you don't specify a notification, SignalFx sends the generic notification.
    """
    host_or_usage_limits: pulumi.Output[dict]
    """
    Specify Usage-based limits for this token.

      * `containerLimit` (`float`) - Max number of Docker containers that can use this token
      * `containerNotificationThreshold` (`float`) - Notification threshold for Docker containers
      * `customMetricsLimit` (`float`) - Max number of custom metrics that can be sent with this token
      * `customMetricsNotificationThreshold` (`float`) - Notification threshold for custom metrics
      * `highResMetricsLimit` (`float`) - Max number of hi-res metrics that can be sent with this toke
      * `highResMetricsNotificationThreshold` (`float`) - Notification threshold for hi-res metrics
      * `hostLimit` (`float`) - Max number of hosts that can use this token
      * `hostNotificationThreshold` (`float`) - Notification threshold for hosts
    """
    name: pulumi.Output[str]
    """
    Name of the token.
    """
    notifications: pulumi.Output[list]
    """
    Where to send notifications about this token's limits. Please consult the `Notification Format` laid out in detectors.
    """
    secret: pulumi.Output[str]
    """
    The secret token created by the API. You cannot set this value.
    """
    def __init__(__self__, resource_name, opts=None, description=None, disabled=None, dpm_limits=None, host_or_usage_limits=None, name=None, notifications=None, __props__=None, __name__=None, __opts__=None):
        """
        Manage SignalFx org tokens.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_signalfx as signalfx

        myteamkey0 = signalfx.OrgToken("myteamkey0",
            description="My team's rad key",
            host_or_usage_limits={
                "containerLimit": 200,
                "containerNotificationThreshold": 180,
                "customMetricsLimit": 1000,
                "customMetricsNotificationThreshold": 900,
                "highResMetricsLimit": 1000,
                "highResMetricsNotificationThreshold": 900,
                "hostLimit": 100,
                "hostNotificationThreshold": 90,
            },
            notifications=["Email,foo-alerts@bar.com"])
        ```


        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the token.
        :param pulumi.Input[bool] disabled: Flag that controls enabling the token. If set to `true`, the token is disabled, and you can't use it for authentication. Defaults to `false`.
        :param pulumi.Input[dict] dpm_limits: Specify DPM-based limits for this token.
        :param pulumi.Input[dict] host_or_usage_limits: Specify Usage-based limits for this token.
        :param pulumi.Input[str] name: Name of the token.
        :param pulumi.Input[list] notifications: Where to send notifications about this token's limits. Please consult the `Notification Format` laid out in detectors.

        The **dpm_limits** object supports the following:

          * `dpmLimit` (`pulumi.Input[float]`) - The datapoints per minute (dpm) limit for this token. If you exceed this limit, SignalFx sends out an alert.
          * `dpmNotificationThreshold` (`pulumi.Input[float]`) - DPM level at which SignalFx sends the notification for this token. If you don't specify a notification, SignalFx sends the generic notification.

        The **host_or_usage_limits** object supports the following:

          * `containerLimit` (`pulumi.Input[float]`) - Max number of Docker containers that can use this token
          * `containerNotificationThreshold` (`pulumi.Input[float]`) - Notification threshold for Docker containers
          * `customMetricsLimit` (`pulumi.Input[float]`) - Max number of custom metrics that can be sent with this token
          * `customMetricsNotificationThreshold` (`pulumi.Input[float]`) - Notification threshold for custom metrics
          * `highResMetricsLimit` (`pulumi.Input[float]`) - Max number of hi-res metrics that can be sent with this toke
          * `highResMetricsNotificationThreshold` (`pulumi.Input[float]`) - Notification threshold for hi-res metrics
          * `hostLimit` (`pulumi.Input[float]`) - Max number of hosts that can use this token
          * `hostNotificationThreshold` (`pulumi.Input[float]`) - Notification threshold for hosts
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['description'] = description
            __props__['disabled'] = disabled
            __props__['dpm_limits'] = dpm_limits
            __props__['host_or_usage_limits'] = host_or_usage_limits
            __props__['name'] = name
            __props__['notifications'] = notifications
            __props__['secret'] = None
        super(OrgToken, __self__).__init__(
            'signalfx:index/orgToken:OrgToken',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, description=None, disabled=None, dpm_limits=None, host_or_usage_limits=None, name=None, notifications=None, secret=None):
        """
        Get an existing OrgToken resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the token.
        :param pulumi.Input[bool] disabled: Flag that controls enabling the token. If set to `true`, the token is disabled, and you can't use it for authentication. Defaults to `false`.
        :param pulumi.Input[dict] dpm_limits: Specify DPM-based limits for this token.
        :param pulumi.Input[dict] host_or_usage_limits: Specify Usage-based limits for this token.
        :param pulumi.Input[str] name: Name of the token.
        :param pulumi.Input[list] notifications: Where to send notifications about this token's limits. Please consult the `Notification Format` laid out in detectors.
        :param pulumi.Input[str] secret: The secret token created by the API. You cannot set this value.

        The **dpm_limits** object supports the following:

          * `dpmLimit` (`pulumi.Input[float]`) - The datapoints per minute (dpm) limit for this token. If you exceed this limit, SignalFx sends out an alert.
          * `dpmNotificationThreshold` (`pulumi.Input[float]`) - DPM level at which SignalFx sends the notification for this token. If you don't specify a notification, SignalFx sends the generic notification.

        The **host_or_usage_limits** object supports the following:

          * `containerLimit` (`pulumi.Input[float]`) - Max number of Docker containers that can use this token
          * `containerNotificationThreshold` (`pulumi.Input[float]`) - Notification threshold for Docker containers
          * `customMetricsLimit` (`pulumi.Input[float]`) - Max number of custom metrics that can be sent with this token
          * `customMetricsNotificationThreshold` (`pulumi.Input[float]`) - Notification threshold for custom metrics
          * `highResMetricsLimit` (`pulumi.Input[float]`) - Max number of hi-res metrics that can be sent with this toke
          * `highResMetricsNotificationThreshold` (`pulumi.Input[float]`) - Notification threshold for hi-res metrics
          * `hostLimit` (`pulumi.Input[float]`) - Max number of hosts that can use this token
          * `hostNotificationThreshold` (`pulumi.Input[float]`) - Notification threshold for hosts
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["description"] = description
        __props__["disabled"] = disabled
        __props__["dpm_limits"] = dpm_limits
        __props__["host_or_usage_limits"] = host_or_usage_limits
        __props__["name"] = name
        __props__["notifications"] = notifications
        __props__["secret"] = secret
        return OrgToken(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

