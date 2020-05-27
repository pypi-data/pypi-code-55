"""
## AWS::GlobalAccelerator Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_globalaccelerator as globalaccelerator
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.core

from ._jsii import *


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAccelerator(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-globalaccelerator.CfnAccelerator"):
    """A CloudFormation ``AWS::GlobalAccelerator::Accelerator``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html
    cloudformationResource:
    :cloudformationResource:: AWS::GlobalAccelerator::Accelerator
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, ip_addresses: typing.Optional[typing.List[str]]=None, ip_address_type: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::GlobalAccelerator::Accelerator``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::GlobalAccelerator::Accelerator.Name``.
        :param enabled: ``AWS::GlobalAccelerator::Accelerator.Enabled``.
        :param ip_addresses: ``AWS::GlobalAccelerator::Accelerator.IpAddresses``.
        :param ip_address_type: ``AWS::GlobalAccelerator::Accelerator.IpAddressType``.
        :param tags: ``AWS::GlobalAccelerator::Accelerator.Tags``.
        """
        props = CfnAcceleratorProps(name=name, enabled=enabled, ip_addresses=ip_addresses, ip_address_type=ip_address_type, tags=tags)

        jsii.create(CfnAccelerator, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnAccelerator":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrAcceleratorArn")
    def attr_accelerator_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: AcceleratorArn
        """
        return jsii.get(self, "attrAcceleratorArn")

    @builtins.property
    @jsii.member(jsii_name="attrDnsName")
    def attr_dns_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DnsName
        """
        return jsii.get(self, "attrDnsName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::GlobalAccelerator::Accelerator.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::GlobalAccelerator::Accelerator.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::GlobalAccelerator::Accelerator.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.Optional[typing.List[str]]:
        """``AWS::GlobalAccelerator::Accelerator.IpAddresses``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresses
        """
        return jsii.get(self, "ipAddresses")

    @ip_addresses.setter
    def ip_addresses(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "ipAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::Accelerator.IpAddressType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresstype
        """
        return jsii.get(self, "ipAddressType")

    @ip_address_type.setter
    def ip_address_type(self, value: typing.Optional[str]):
        jsii.set(self, "ipAddressType", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-globalaccelerator.CfnAcceleratorProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'enabled': 'enabled', 'ip_addresses': 'ipAddresses', 'ip_address_type': 'ipAddressType', 'tags': 'tags'})
class CfnAcceleratorProps():
    def __init__(self, *, name: str, enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, ip_addresses: typing.Optional[typing.List[str]]=None, ip_address_type: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::GlobalAccelerator::Accelerator``.

        :param name: ``AWS::GlobalAccelerator::Accelerator.Name``.
        :param enabled: ``AWS::GlobalAccelerator::Accelerator.Enabled``.
        :param ip_addresses: ``AWS::GlobalAccelerator::Accelerator.IpAddresses``.
        :param ip_address_type: ``AWS::GlobalAccelerator::Accelerator.IpAddressType``.
        :param tags: ``AWS::GlobalAccelerator::Accelerator.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html
        """
        self._values = {
            'name': name,
        }
        if enabled is not None: self._values["enabled"] = enabled
        if ip_addresses is not None: self._values["ip_addresses"] = ip_addresses
        if ip_address_type is not None: self._values["ip_address_type"] = ip_address_type
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def name(self) -> str:
        """``AWS::GlobalAccelerator::Accelerator.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-name
        """
        return self._values.get('name')

    @builtins.property
    def enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::GlobalAccelerator::Accelerator.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-enabled
        """
        return self._values.get('enabled')

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[str]]:
        """``AWS::GlobalAccelerator::Accelerator.IpAddresses``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresses
        """
        return self._values.get('ip_addresses')

    @builtins.property
    def ip_address_type(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::Accelerator.IpAddressType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresstype
        """
        return self._values.get('ip_address_type')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::GlobalAccelerator::Accelerator.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAcceleratorProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEndpointGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroup"):
    """A CloudFormation ``AWS::GlobalAccelerator::EndpointGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::GlobalAccelerator::EndpointGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, endpoint_group_region: str, listener_arn: str, endpoint_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "EndpointConfigurationProperty"]]]]]=None, health_check_interval_seconds: typing.Optional[jsii.Number]=None, health_check_path: typing.Optional[str]=None, health_check_port: typing.Optional[jsii.Number]=None, health_check_protocol: typing.Optional[str]=None, threshold_count: typing.Optional[jsii.Number]=None, traffic_dial_percentage: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::GlobalAccelerator::EndpointGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param endpoint_group_region: ``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.
        :param listener_arn: ``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.
        :param endpoint_configurations: ``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.
        :param health_check_interval_seconds: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.
        :param threshold_count: ``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.
        :param traffic_dial_percentage: ``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.
        """
        props = CfnEndpointGroupProps(endpoint_group_region=endpoint_group_region, listener_arn=listener_arn, endpoint_configurations=endpoint_configurations, health_check_interval_seconds=health_check_interval_seconds, health_check_path=health_check_path, health_check_port=health_check_port, health_check_protocol=health_check_protocol, threshold_count=threshold_count, traffic_dial_percentage=traffic_dial_percentage)

        jsii.create(CfnEndpointGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnEndpointGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrEndpointGroupArn")
    def attr_endpoint_group_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: EndpointGroupArn
        """
        return jsii.get(self, "attrEndpointGroupArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="endpointGroupRegion")
    def endpoint_group_region(self) -> str:
        """``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointgroupregion
        """
        return jsii.get(self, "endpointGroupRegion")

    @endpoint_group_region.setter
    def endpoint_group_region(self, value: str):
        jsii.set(self, "endpointGroupRegion", value)

    @builtins.property
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> str:
        """``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-listenerarn
        """
        return jsii.get(self, "listenerArn")

    @listener_arn.setter
    def listener_arn(self, value: str):
        jsii.set(self, "listenerArn", value)

    @builtins.property
    @jsii.member(jsii_name="endpointConfigurations")
    def endpoint_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "EndpointConfigurationProperty"]]]]]:
        """``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointconfigurations
        """
        return jsii.get(self, "endpointConfigurations")

    @endpoint_configurations.setter
    def endpoint_configurations(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "EndpointConfigurationProperty"]]]]]):
        jsii.set(self, "endpointConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckintervalseconds
        """
        return jsii.get(self, "healthCheckIntervalSeconds")

    @health_check_interval_seconds.setter
    def health_check_interval_seconds(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "healthCheckIntervalSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckpath
        """
        return jsii.get(self, "healthCheckPath")

    @health_check_path.setter
    def health_check_path(self, value: typing.Optional[str]):
        jsii.set(self, "healthCheckPath", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckPort")
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckport
        """
        return jsii.get(self, "healthCheckPort")

    @health_check_port.setter
    def health_check_port(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "healthCheckPort", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckProtocol")
    def health_check_protocol(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckprotocol
        """
        return jsii.get(self, "healthCheckProtocol")

    @health_check_protocol.setter
    def health_check_protocol(self, value: typing.Optional[str]):
        jsii.set(self, "healthCheckProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="thresholdCount")
    def threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-thresholdcount
        """
        return jsii.get(self, "thresholdCount")

    @threshold_count.setter
    def threshold_count(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "thresholdCount", value)

    @builtins.property
    @jsii.member(jsii_name="trafficDialPercentage")
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-trafficdialpercentage
        """
        return jsii.get(self, "trafficDialPercentage")

    @traffic_dial_percentage.setter
    def traffic_dial_percentage(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "trafficDialPercentage", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroup.EndpointConfigurationProperty", jsii_struct_bases=[], name_mapping={'endpoint_id': 'endpointId', 'client_ip_preservation_enabled': 'clientIpPreservationEnabled', 'weight': 'weight'})
    class EndpointConfigurationProperty():
        def __init__(self, *, endpoint_id: str, client_ip_preservation_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, weight: typing.Optional[jsii.Number]=None) -> None:
            """
            :param endpoint_id: ``CfnEndpointGroup.EndpointConfigurationProperty.EndpointId``.
            :param client_ip_preservation_enabled: ``CfnEndpointGroup.EndpointConfigurationProperty.ClientIPPreservationEnabled``.
            :param weight: ``CfnEndpointGroup.EndpointConfigurationProperty.Weight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html
            """
            self._values = {
                'endpoint_id': endpoint_id,
            }
            if client_ip_preservation_enabled is not None: self._values["client_ip_preservation_enabled"] = client_ip_preservation_enabled
            if weight is not None: self._values["weight"] = weight

        @builtins.property
        def endpoint_id(self) -> str:
            """``CfnEndpointGroup.EndpointConfigurationProperty.EndpointId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-endpointid
            """
            return self._values.get('endpoint_id')

        @builtins.property
        def client_ip_preservation_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnEndpointGroup.EndpointConfigurationProperty.ClientIPPreservationEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-clientippreservationenabled
            """
            return self._values.get('client_ip_preservation_enabled')

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            """``CfnEndpointGroup.EndpointConfigurationProperty.Weight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-weight
            """
            return self._values.get('weight')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EndpointConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroupProps", jsii_struct_bases=[], name_mapping={'endpoint_group_region': 'endpointGroupRegion', 'listener_arn': 'listenerArn', 'endpoint_configurations': 'endpointConfigurations', 'health_check_interval_seconds': 'healthCheckIntervalSeconds', 'health_check_path': 'healthCheckPath', 'health_check_port': 'healthCheckPort', 'health_check_protocol': 'healthCheckProtocol', 'threshold_count': 'thresholdCount', 'traffic_dial_percentage': 'trafficDialPercentage'})
class CfnEndpointGroupProps():
    def __init__(self, *, endpoint_group_region: str, listener_arn: str, endpoint_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.EndpointConfigurationProperty"]]]]]=None, health_check_interval_seconds: typing.Optional[jsii.Number]=None, health_check_path: typing.Optional[str]=None, health_check_port: typing.Optional[jsii.Number]=None, health_check_protocol: typing.Optional[str]=None, threshold_count: typing.Optional[jsii.Number]=None, traffic_dial_percentage: typing.Optional[jsii.Number]=None) -> None:
        """Properties for defining a ``AWS::GlobalAccelerator::EndpointGroup``.

        :param endpoint_group_region: ``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.
        :param listener_arn: ``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.
        :param endpoint_configurations: ``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.
        :param health_check_interval_seconds: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.
        :param threshold_count: ``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.
        :param traffic_dial_percentage: ``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html
        """
        self._values = {
            'endpoint_group_region': endpoint_group_region,
            'listener_arn': listener_arn,
        }
        if endpoint_configurations is not None: self._values["endpoint_configurations"] = endpoint_configurations
        if health_check_interval_seconds is not None: self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None: self._values["health_check_path"] = health_check_path
        if health_check_port is not None: self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None: self._values["health_check_protocol"] = health_check_protocol
        if threshold_count is not None: self._values["threshold_count"] = threshold_count
        if traffic_dial_percentage is not None: self._values["traffic_dial_percentage"] = traffic_dial_percentage

    @builtins.property
    def endpoint_group_region(self) -> str:
        """``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointgroupregion
        """
        return self._values.get('endpoint_group_region')

    @builtins.property
    def listener_arn(self) -> str:
        """``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-listenerarn
        """
        return self._values.get('listener_arn')

    @builtins.property
    def endpoint_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.EndpointConfigurationProperty"]]]]]:
        """``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointconfigurations
        """
        return self._values.get('endpoint_configurations')

    @builtins.property
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckintervalseconds
        """
        return self._values.get('health_check_interval_seconds')

    @builtins.property
    def health_check_path(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckpath
        """
        return self._values.get('health_check_path')

    @builtins.property
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckport
        """
        return self._values.get('health_check_port')

    @builtins.property
    def health_check_protocol(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckprotocol
        """
        return self._values.get('health_check_protocol')

    @builtins.property
    def threshold_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-thresholdcount
        """
        return self._values.get('threshold_count')

    @builtins.property
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        """``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-trafficdialpercentage
        """
        return self._values.get('traffic_dial_percentage')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnEndpointGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnListener(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-globalaccelerator.CfnListener"):
    """A CloudFormation ``AWS::GlobalAccelerator::Listener``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html
    cloudformationResource:
    :cloudformationResource:: AWS::GlobalAccelerator::Listener
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, accelerator_arn: str, port_ranges: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "PortRangeProperty"]]], protocol: str, client_affinity: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GlobalAccelerator::Listener``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param accelerator_arn: ``AWS::GlobalAccelerator::Listener.AcceleratorArn``.
        :param port_ranges: ``AWS::GlobalAccelerator::Listener.PortRanges``.
        :param protocol: ``AWS::GlobalAccelerator::Listener.Protocol``.
        :param client_affinity: ``AWS::GlobalAccelerator::Listener.ClientAffinity``.
        """
        props = CfnListenerProps(accelerator_arn=accelerator_arn, port_ranges=port_ranges, protocol=protocol, client_affinity=client_affinity)

        jsii.create(CfnListener, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnListener":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrListenerArn")
    def attr_listener_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ListenerArn
        """
        return jsii.get(self, "attrListenerArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> str:
        """``AWS::GlobalAccelerator::Listener.AcceleratorArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-acceleratorarn
        """
        return jsii.get(self, "acceleratorArn")

    @accelerator_arn.setter
    def accelerator_arn(self, value: str):
        jsii.set(self, "acceleratorArn", value)

    @builtins.property
    @jsii.member(jsii_name="portRanges")
    def port_ranges(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "PortRangeProperty"]]]:
        """``AWS::GlobalAccelerator::Listener.PortRanges``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-portranges
        """
        return jsii.get(self, "portRanges")

    @port_ranges.setter
    def port_ranges(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "PortRangeProperty"]]]):
        jsii.set(self, "portRanges", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> str:
        """``AWS::GlobalAccelerator::Listener.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-protocol
        """
        return jsii.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: str):
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="clientAffinity")
    def client_affinity(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-clientaffinity
        """
        return jsii.get(self, "clientAffinity")

    @client_affinity.setter
    def client_affinity(self, value: typing.Optional[str]):
        jsii.set(self, "clientAffinity", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-globalaccelerator.CfnListener.PortRangeProperty", jsii_struct_bases=[], name_mapping={'from_port': 'fromPort', 'to_port': 'toPort'})
    class PortRangeProperty():
        def __init__(self, *, from_port: jsii.Number, to_port: jsii.Number) -> None:
            """
            :param from_port: ``CfnListener.PortRangeProperty.FromPort``.
            :param to_port: ``CfnListener.PortRangeProperty.ToPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html
            """
            self._values = {
                'from_port': from_port,
                'to_port': to_port,
            }

        @builtins.property
        def from_port(self) -> jsii.Number:
            """``CfnListener.PortRangeProperty.FromPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html#cfn-globalaccelerator-listener-portrange-fromport
            """
            return self._values.get('from_port')

        @builtins.property
        def to_port(self) -> jsii.Number:
            """``CfnListener.PortRangeProperty.ToPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html#cfn-globalaccelerator-listener-portrange-toport
            """
            return self._values.get('to_port')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PortRangeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-globalaccelerator.CfnListenerProps", jsii_struct_bases=[], name_mapping={'accelerator_arn': 'acceleratorArn', 'port_ranges': 'portRanges', 'protocol': 'protocol', 'client_affinity': 'clientAffinity'})
class CfnListenerProps():
    def __init__(self, *, accelerator_arn: str, port_ranges: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.PortRangeProperty"]]], protocol: str, client_affinity: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::GlobalAccelerator::Listener``.

        :param accelerator_arn: ``AWS::GlobalAccelerator::Listener.AcceleratorArn``.
        :param port_ranges: ``AWS::GlobalAccelerator::Listener.PortRanges``.
        :param protocol: ``AWS::GlobalAccelerator::Listener.Protocol``.
        :param client_affinity: ``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html
        """
        self._values = {
            'accelerator_arn': accelerator_arn,
            'port_ranges': port_ranges,
            'protocol': protocol,
        }
        if client_affinity is not None: self._values["client_affinity"] = client_affinity

    @builtins.property
    def accelerator_arn(self) -> str:
        """``AWS::GlobalAccelerator::Listener.AcceleratorArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-acceleratorarn
        """
        return self._values.get('accelerator_arn')

    @builtins.property
    def port_ranges(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.PortRangeProperty"]]]:
        """``AWS::GlobalAccelerator::Listener.PortRanges``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-portranges
        """
        return self._values.get('port_ranges')

    @builtins.property
    def protocol(self) -> str:
        """``AWS::GlobalAccelerator::Listener.Protocol``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-protocol
        """
        return self._values.get('protocol')

    @builtins.property
    def client_affinity(self) -> typing.Optional[str]:
        """``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-clientaffinity
        """
        return self._values.get('client_affinity')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnAccelerator",
    "CfnAcceleratorProps",
    "CfnEndpointGroup",
    "CfnEndpointGroupProps",
    "CfnListener",
    "CfnListenerProps",
]

publication.publish()
