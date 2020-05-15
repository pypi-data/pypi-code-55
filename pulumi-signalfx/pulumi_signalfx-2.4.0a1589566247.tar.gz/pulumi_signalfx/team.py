# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class Team(pulumi.CustomResource):
    description: pulumi.Output[str]
    """
    Description of the team.
    """
    members: pulumi.Output[list]
    """
    List of user IDs to include in the team.
    """
    name: pulumi.Output[str]
    """
    Name of the team.
    """
    notifications_criticals: pulumi.Output[list]
    """
    Where to send notifications for critical alerts
    """
    notifications_defaults: pulumi.Output[list]
    """
    Where to send notifications for default alerts
    """
    notifications_infos: pulumi.Output[list]
    """
    Where to send notifications for info alerts
    """
    notifications_majors: pulumi.Output[list]
    """
    Where to send notifications for major alerts
    """
    notifications_minors: pulumi.Output[list]
    """
    Where to send notifications for minor alerts
    """
    notifications_warnings: pulumi.Output[list]
    """
    Where to send notifications for warning alerts
    """
    url: pulumi.Output[str]
    """
    URL of the team
    """
    def __init__(__self__, resource_name, opts=None, description=None, members=None, name=None, notifications_criticals=None, notifications_defaults=None, notifications_infos=None, notifications_majors=None, notifications_minors=None, notifications_warnings=None, __props__=None, __name__=None, __opts__=None):
        """
        Handles management of SignalFx teams.

        You can configure [team notification policies](https://docs.signalfx.com/en/latest/managing/teams/team-notifications.html) using this resource and the various `notifications_*` properties.



        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the team.
        :param pulumi.Input[list] members: List of user IDs to include in the team.
        :param pulumi.Input[str] name: Name of the team.
        :param pulumi.Input[list] notifications_criticals: Where to send notifications for critical alerts
        :param pulumi.Input[list] notifications_defaults: Where to send notifications for default alerts
        :param pulumi.Input[list] notifications_infos: Where to send notifications for info alerts
        :param pulumi.Input[list] notifications_majors: Where to send notifications for major alerts
        :param pulumi.Input[list] notifications_minors: Where to send notifications for minor alerts
        :param pulumi.Input[list] notifications_warnings: Where to send notifications for warning alerts
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
            __props__['members'] = members
            __props__['name'] = name
            __props__['notifications_criticals'] = notifications_criticals
            __props__['notifications_defaults'] = notifications_defaults
            __props__['notifications_infos'] = notifications_infos
            __props__['notifications_majors'] = notifications_majors
            __props__['notifications_minors'] = notifications_minors
            __props__['notifications_warnings'] = notifications_warnings
            __props__['url'] = None
        super(Team, __self__).__init__(
            'signalfx:index/team:Team',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, description=None, members=None, name=None, notifications_criticals=None, notifications_defaults=None, notifications_infos=None, notifications_majors=None, notifications_minors=None, notifications_warnings=None, url=None):
        """
        Get an existing Team resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the team.
        :param pulumi.Input[list] members: List of user IDs to include in the team.
        :param pulumi.Input[str] name: Name of the team.
        :param pulumi.Input[list] notifications_criticals: Where to send notifications for critical alerts
        :param pulumi.Input[list] notifications_defaults: Where to send notifications for default alerts
        :param pulumi.Input[list] notifications_infos: Where to send notifications for info alerts
        :param pulumi.Input[list] notifications_majors: Where to send notifications for major alerts
        :param pulumi.Input[list] notifications_minors: Where to send notifications for minor alerts
        :param pulumi.Input[list] notifications_warnings: Where to send notifications for warning alerts
        :param pulumi.Input[str] url: URL of the team
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["description"] = description
        __props__["members"] = members
        __props__["name"] = name
        __props__["notifications_criticals"] = notifications_criticals
        __props__["notifications_defaults"] = notifications_defaults
        __props__["notifications_infos"] = notifications_infos
        __props__["notifications_majors"] = notifications_majors
        __props__["notifications_minors"] = notifications_minors
        __props__["notifications_warnings"] = notifications_warnings
        __props__["url"] = url
        return Team(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

