"""
## Amazon Neptune Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_neptune as neptune
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
import constructs

from ._jsii import *


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDBCluster(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-neptune.CfnDBCluster"):
    """A CloudFormation ``AWS::Neptune::DBCluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::Neptune::DBCluster
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, availability_zones: typing.Optional[typing.List[str]]=None, backup_retention_period: typing.Optional[jsii.Number]=None, db_cluster_identifier: typing.Optional[str]=None, db_cluster_parameter_group_name: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, deletion_protection: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]]=None, engine_version: typing.Optional[str]=None, iam_auth_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, kms_key_id: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, preferred_backup_window: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, snapshot_identifier: typing.Optional[str]=None, storage_encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::Neptune::DBCluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param availability_zones: ``AWS::Neptune::DBCluster.AvailabilityZones``.
        :param backup_retention_period: ``AWS::Neptune::DBCluster.BackupRetentionPeriod``.
        :param db_cluster_identifier: ``AWS::Neptune::DBCluster.DBClusterIdentifier``.
        :param db_cluster_parameter_group_name: ``AWS::Neptune::DBCluster.DBClusterParameterGroupName``.
        :param db_subnet_group_name: ``AWS::Neptune::DBCluster.DBSubnetGroupName``.
        :param deletion_protection: ``AWS::Neptune::DBCluster.DeletionProtection``.
        :param enable_cloudwatch_logs_exports: ``AWS::Neptune::DBCluster.EnableCloudwatchLogsExports``.
        :param engine_version: ``AWS::Neptune::DBCluster.EngineVersion``.
        :param iam_auth_enabled: ``AWS::Neptune::DBCluster.IamAuthEnabled``.
        :param kms_key_id: ``AWS::Neptune::DBCluster.KmsKeyId``.
        :param port: ``AWS::Neptune::DBCluster.Port``.
        :param preferred_backup_window: ``AWS::Neptune::DBCluster.PreferredBackupWindow``.
        :param preferred_maintenance_window: ``AWS::Neptune::DBCluster.PreferredMaintenanceWindow``.
        :param snapshot_identifier: ``AWS::Neptune::DBCluster.SnapshotIdentifier``.
        :param storage_encrypted: ``AWS::Neptune::DBCluster.StorageEncrypted``.
        :param tags: ``AWS::Neptune::DBCluster.Tags``.
        :param vpc_security_group_ids: ``AWS::Neptune::DBCluster.VpcSecurityGroupIds``.
        """
        props = CfnDBClusterProps(availability_zones=availability_zones, backup_retention_period=backup_retention_period, db_cluster_identifier=db_cluster_identifier, db_cluster_parameter_group_name=db_cluster_parameter_group_name, db_subnet_group_name=db_subnet_group_name, deletion_protection=deletion_protection, enable_cloudwatch_logs_exports=enable_cloudwatch_logs_exports, engine_version=engine_version, iam_auth_enabled=iam_auth_enabled, kms_key_id=kms_key_id, port=port, preferred_backup_window=preferred_backup_window, preferred_maintenance_window=preferred_maintenance_window, snapshot_identifier=snapshot_identifier, storage_encrypted=storage_encrypted, tags=tags, vpc_security_group_ids=vpc_security_group_ids)

        jsii.create(CfnDBCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any) -> "CfnDBCluster":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes])

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
    @jsii.member(jsii_name="attrClusterResourceId")
    def attr_cluster_resource_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ClusterResourceId
        """
        return jsii.get(self, "attrClusterResourceId")

    @builtins.property
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint
        """
        return jsii.get(self, "attrEndpoint")

    @builtins.property
    @jsii.member(jsii_name="attrPort")
    def attr_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Port
        """
        return jsii.get(self, "attrPort")

    @builtins.property
    @jsii.member(jsii_name="attrReadEndpoint")
    def attr_read_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ReadEndpoint
        """
        return jsii.get(self, "attrReadEndpoint")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Neptune::DBCluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Neptune::DBCluster.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-availabilityzones
        """
        return jsii.get(self, "availabilityZones")

    @availability_zones.setter
    def availability_zones(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "availabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="backupRetentionPeriod")
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Neptune::DBCluster.BackupRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-backupretentionperiod
        """
        return jsii.get(self, "backupRetentionPeriod")

    @backup_retention_period.setter
    def backup_retention_period(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "backupRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbclusteridentifier
        """
        return jsii.get(self, "dbClusterIdentifier")

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: typing.Optional[str]):
        jsii.set(self, "dbClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterParameterGroupName")
    def db_cluster_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.DBClusterParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbclusterparametergroupname
        """
        return jsii.get(self, "dbClusterParameterGroupName")

    @db_cluster_parameter_group_name.setter
    def db_cluster_parameter_group_name(self, value: typing.Optional[str]):
        jsii.set(self, "dbClusterParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbsubnetgroupname
        """
        return jsii.get(self, "dbSubnetGroupName")

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[str]):
        jsii.set(self, "dbSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Neptune::DBCluster.DeletionProtection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-deletionprotection
        """
        return jsii.get(self, "deletionProtection")

    @deletion_protection.setter
    def deletion_protection(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "deletionProtection", value)

    @builtins.property
    @jsii.member(jsii_name="enableCloudwatchLogsExports")
    def enable_cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Neptune::DBCluster.EnableCloudwatchLogsExports``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-enablecloudwatchlogsexports
        """
        return jsii.get(self, "enableCloudwatchLogsExports")

    @enable_cloudwatch_logs_exports.setter
    def enable_cloudwatch_logs_exports(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "enableCloudwatchLogsExports", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter
    def engine_version(self, value: typing.Optional[str]):
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="iamAuthEnabled")
    def iam_auth_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Neptune::DBCluster.IamAuthEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-iamauthenabled
        """
        return jsii.get(self, "iamAuthEnabled")

    @iam_auth_enabled.setter
    def iam_auth_enabled(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "iamAuthEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]):
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::Neptune::DBCluster.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-port
        """
        return jsii.get(self, "port")

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="preferredBackupWindow")
    def preferred_backup_window(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.PreferredBackupWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-preferredbackupwindow
        """
        return jsii.get(self, "preferredBackupWindow")

    @preferred_backup_window.setter
    def preferred_backup_window(self, value: typing.Optional[str]):
        jsii.set(self, "preferredBackupWindow", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: typing.Optional[str]):
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotIdentifier")
    def snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.SnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-snapshotidentifier
        """
        return jsii.get(self, "snapshotIdentifier")

    @snapshot_identifier.setter
    def snapshot_identifier(self, value: typing.Optional[str]):
        jsii.set(self, "snapshotIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="storageEncrypted")
    def storage_encrypted(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Neptune::DBCluster.StorageEncrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-storageencrypted
        """
        return jsii.get(self, "storageEncrypted")

    @storage_encrypted.setter
    def storage_encrypted(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "storageEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Neptune::DBCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-vpcsecuritygroupids
        """
        return jsii.get(self, "vpcSecurityGroupIds")

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(self, value: typing.Optional[typing.List[str]]):
        jsii.set(self, "vpcSecurityGroupIds", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDBClusterParameterGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-neptune.CfnDBClusterParameterGroup"):
    """A CloudFormation ``AWS::Neptune::DBClusterParameterGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Neptune::DBClusterParameterGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: str, family: str, parameters: typing.Any, name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::Neptune::DBClusterParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Neptune::DBClusterParameterGroup.Description``.
        :param family: ``AWS::Neptune::DBClusterParameterGroup.Family``.
        :param parameters: ``AWS::Neptune::DBClusterParameterGroup.Parameters``.
        :param name: ``AWS::Neptune::DBClusterParameterGroup.Name``.
        :param tags: ``AWS::Neptune::DBClusterParameterGroup.Tags``.
        """
        props = CfnDBClusterParameterGroupProps(description=description, family=family, parameters=parameters, name=name, tags=tags)

        jsii.create(CfnDBClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any) -> "CfnDBClusterParameterGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Neptune::DBClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::Neptune::DBClusterParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> str:
        """``AWS::Neptune::DBClusterParameterGroup.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-family
        """
        return jsii.get(self, "family")

    @family.setter
    def family(self, value: str):
        jsii.set(self, "family", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        """``AWS::Neptune::DBClusterParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: typing.Any):
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBClusterParameterGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-neptune.CfnDBClusterParameterGroupProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'family': 'family', 'parameters': 'parameters', 'name': 'name', 'tags': 'tags'})
class CfnDBClusterParameterGroupProps():
    def __init__(self, *, description: str, family: str, parameters: typing.Any, name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::Neptune::DBClusterParameterGroup``.

        :param description: ``AWS::Neptune::DBClusterParameterGroup.Description``.
        :param family: ``AWS::Neptune::DBClusterParameterGroup.Family``.
        :param parameters: ``AWS::Neptune::DBClusterParameterGroup.Parameters``.
        :param name: ``AWS::Neptune::DBClusterParameterGroup.Name``.
        :param tags: ``AWS::Neptune::DBClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html
        """
        self._values = {
            'description': description,
            'family': family,
            'parameters': parameters,
        }
        if name is not None: self._values["name"] = name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def description(self) -> str:
        """``AWS::Neptune::DBClusterParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-description
        """
        return self._values.get('description')

    @builtins.property
    def family(self) -> str:
        """``AWS::Neptune::DBClusterParameterGroup.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-family
        """
        return self._values.get('family')

    @builtins.property
    def parameters(self) -> typing.Any:
        """``AWS::Neptune::DBClusterParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-parameters
        """
        return self._values.get('parameters')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBClusterParameterGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-name
        """
        return self._values.get('name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Neptune::DBClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDBClusterParameterGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-neptune.CfnDBClusterProps", jsii_struct_bases=[], name_mapping={'availability_zones': 'availabilityZones', 'backup_retention_period': 'backupRetentionPeriod', 'db_cluster_identifier': 'dbClusterIdentifier', 'db_cluster_parameter_group_name': 'dbClusterParameterGroupName', 'db_subnet_group_name': 'dbSubnetGroupName', 'deletion_protection': 'deletionProtection', 'enable_cloudwatch_logs_exports': 'enableCloudwatchLogsExports', 'engine_version': 'engineVersion', 'iam_auth_enabled': 'iamAuthEnabled', 'kms_key_id': 'kmsKeyId', 'port': 'port', 'preferred_backup_window': 'preferredBackupWindow', 'preferred_maintenance_window': 'preferredMaintenanceWindow', 'snapshot_identifier': 'snapshotIdentifier', 'storage_encrypted': 'storageEncrypted', 'tags': 'tags', 'vpc_security_group_ids': 'vpcSecurityGroupIds'})
class CfnDBClusterProps():
    def __init__(self, *, availability_zones: typing.Optional[typing.List[str]]=None, backup_retention_period: typing.Optional[jsii.Number]=None, db_cluster_identifier: typing.Optional[str]=None, db_cluster_parameter_group_name: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, deletion_protection: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]]=None, engine_version: typing.Optional[str]=None, iam_auth_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, kms_key_id: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, preferred_backup_window: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, snapshot_identifier: typing.Optional[str]=None, storage_encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        """Properties for defining a ``AWS::Neptune::DBCluster``.

        :param availability_zones: ``AWS::Neptune::DBCluster.AvailabilityZones``.
        :param backup_retention_period: ``AWS::Neptune::DBCluster.BackupRetentionPeriod``.
        :param db_cluster_identifier: ``AWS::Neptune::DBCluster.DBClusterIdentifier``.
        :param db_cluster_parameter_group_name: ``AWS::Neptune::DBCluster.DBClusterParameterGroupName``.
        :param db_subnet_group_name: ``AWS::Neptune::DBCluster.DBSubnetGroupName``.
        :param deletion_protection: ``AWS::Neptune::DBCluster.DeletionProtection``.
        :param enable_cloudwatch_logs_exports: ``AWS::Neptune::DBCluster.EnableCloudwatchLogsExports``.
        :param engine_version: ``AWS::Neptune::DBCluster.EngineVersion``.
        :param iam_auth_enabled: ``AWS::Neptune::DBCluster.IamAuthEnabled``.
        :param kms_key_id: ``AWS::Neptune::DBCluster.KmsKeyId``.
        :param port: ``AWS::Neptune::DBCluster.Port``.
        :param preferred_backup_window: ``AWS::Neptune::DBCluster.PreferredBackupWindow``.
        :param preferred_maintenance_window: ``AWS::Neptune::DBCluster.PreferredMaintenanceWindow``.
        :param snapshot_identifier: ``AWS::Neptune::DBCluster.SnapshotIdentifier``.
        :param storage_encrypted: ``AWS::Neptune::DBCluster.StorageEncrypted``.
        :param tags: ``AWS::Neptune::DBCluster.Tags``.
        :param vpc_security_group_ids: ``AWS::Neptune::DBCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html
        """
        self._values = {
        }
        if availability_zones is not None: self._values["availability_zones"] = availability_zones
        if backup_retention_period is not None: self._values["backup_retention_period"] = backup_retention_period
        if db_cluster_identifier is not None: self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_cluster_parameter_group_name is not None: self._values["db_cluster_parameter_group_name"] = db_cluster_parameter_group_name
        if db_subnet_group_name is not None: self._values["db_subnet_group_name"] = db_subnet_group_name
        if deletion_protection is not None: self._values["deletion_protection"] = deletion_protection
        if enable_cloudwatch_logs_exports is not None: self._values["enable_cloudwatch_logs_exports"] = enable_cloudwatch_logs_exports
        if engine_version is not None: self._values["engine_version"] = engine_version
        if iam_auth_enabled is not None: self._values["iam_auth_enabled"] = iam_auth_enabled
        if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
        if port is not None: self._values["port"] = port
        if preferred_backup_window is not None: self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None: self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if snapshot_identifier is not None: self._values["snapshot_identifier"] = snapshot_identifier
        if storage_encrypted is not None: self._values["storage_encrypted"] = storage_encrypted
        if tags is not None: self._values["tags"] = tags
        if vpc_security_group_ids is not None: self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Neptune::DBCluster.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-availabilityzones
        """
        return self._values.get('availability_zones')

    @builtins.property
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Neptune::DBCluster.BackupRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-backupretentionperiod
        """
        return self._values.get('backup_retention_period')

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbclusteridentifier
        """
        return self._values.get('db_cluster_identifier')

    @builtins.property
    def db_cluster_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.DBClusterParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbclusterparametergroupname
        """
        return self._values.get('db_cluster_parameter_group_name')

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbsubnetgroupname
        """
        return self._values.get('db_subnet_group_name')

    @builtins.property
    def deletion_protection(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Neptune::DBCluster.DeletionProtection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-deletionprotection
        """
        return self._values.get('deletion_protection')

    @builtins.property
    def enable_cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Neptune::DBCluster.EnableCloudwatchLogsExports``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-enablecloudwatchlogsexports
        """
        return self._values.get('enable_cloudwatch_logs_exports')

    @builtins.property
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-engineversion
        """
        return self._values.get('engine_version')

    @builtins.property
    def iam_auth_enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Neptune::DBCluster.IamAuthEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-iamauthenabled
        """
        return self._values.get('iam_auth_enabled')

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-kmskeyid
        """
        return self._values.get('kms_key_id')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::Neptune::DBCluster.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-port
        """
        return self._values.get('port')

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.PreferredBackupWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-preferredbackupwindow
        """
        return self._values.get('preferred_backup_window')

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-preferredmaintenancewindow
        """
        return self._values.get('preferred_maintenance_window')

    @builtins.property
    def snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBCluster.SnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-snapshotidentifier
        """
        return self._values.get('snapshot_identifier')

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Neptune::DBCluster.StorageEncrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-storageencrypted
        """
        return self._values.get('storage_encrypted')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Neptune::DBCluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-tags
        """
        return self._values.get('tags')

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Neptune::DBCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-vpcsecuritygroupids
        """
        return self._values.get('vpc_security_group_ids')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDBClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDBInstance(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-neptune.CfnDBInstance"):
    """A CloudFormation ``AWS::Neptune::DBInstance``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html
    cloudformationResource:
    :cloudformationResource:: AWS::Neptune::DBInstance
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, db_instance_class: str, allow_major_version_upgrade: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, auto_minor_version_upgrade: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, availability_zone: typing.Optional[str]=None, db_cluster_identifier: typing.Optional[str]=None, db_instance_identifier: typing.Optional[str]=None, db_parameter_group_name: typing.Optional[str]=None, db_snapshot_identifier: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::Neptune::DBInstance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_instance_class: ``AWS::Neptune::DBInstance.DBInstanceClass``.
        :param allow_major_version_upgrade: ``AWS::Neptune::DBInstance.AllowMajorVersionUpgrade``.
        :param auto_minor_version_upgrade: ``AWS::Neptune::DBInstance.AutoMinorVersionUpgrade``.
        :param availability_zone: ``AWS::Neptune::DBInstance.AvailabilityZone``.
        :param db_cluster_identifier: ``AWS::Neptune::DBInstance.DBClusterIdentifier``.
        :param db_instance_identifier: ``AWS::Neptune::DBInstance.DBInstanceIdentifier``.
        :param db_parameter_group_name: ``AWS::Neptune::DBInstance.DBParameterGroupName``.
        :param db_snapshot_identifier: ``AWS::Neptune::DBInstance.DBSnapshotIdentifier``.
        :param db_subnet_group_name: ``AWS::Neptune::DBInstance.DBSubnetGroupName``.
        :param preferred_maintenance_window: ``AWS::Neptune::DBInstance.PreferredMaintenanceWindow``.
        :param tags: ``AWS::Neptune::DBInstance.Tags``.
        """
        props = CfnDBInstanceProps(db_instance_class=db_instance_class, allow_major_version_upgrade=allow_major_version_upgrade, auto_minor_version_upgrade=auto_minor_version_upgrade, availability_zone=availability_zone, db_cluster_identifier=db_cluster_identifier, db_instance_identifier=db_instance_identifier, db_parameter_group_name=db_parameter_group_name, db_snapshot_identifier=db_snapshot_identifier, db_subnet_group_name=db_subnet_group_name, preferred_maintenance_window=preferred_maintenance_window, tags=tags)

        jsii.create(CfnDBInstance, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any) -> "CfnDBInstance":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes])

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
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint
        """
        return jsii.get(self, "attrEndpoint")

    @builtins.property
    @jsii.member(jsii_name="attrPort")
    def attr_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Port
        """
        return jsii.get(self, "attrPort")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Neptune::DBInstance.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceClass")
    def db_instance_class(self) -> str:
        """``AWS::Neptune::DBInstance.DBInstanceClass``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbinstanceclass
        """
        return jsii.get(self, "dbInstanceClass")

    @db_instance_class.setter
    def db_instance_class(self, value: str):
        jsii.set(self, "dbInstanceClass", value)

    @builtins.property
    @jsii.member(jsii_name="allowMajorVersionUpgrade")
    def allow_major_version_upgrade(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Neptune::DBInstance.AllowMajorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-allowmajorversionupgrade
        """
        return jsii.get(self, "allowMajorVersionUpgrade")

    @allow_major_version_upgrade.setter
    def allow_major_version_upgrade(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "allowMajorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Neptune::DBInstance.AutoMinorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-autominorversionupgrade
        """
        return jsii.get(self, "autoMinorVersionUpgrade")

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.AvailabilityZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-availabilityzone
        """
        return jsii.get(self, "availabilityZone")

    @availability_zone.setter
    def availability_zone(self, value: typing.Optional[str]):
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbclusteridentifier
        """
        return jsii.get(self, "dbClusterIdentifier")

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: typing.Optional[str]):
        jsii.set(self, "dbClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbInstanceIdentifier")
    def db_instance_identifier(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.DBInstanceIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbinstanceidentifier
        """
        return jsii.get(self, "dbInstanceIdentifier")

    @db_instance_identifier.setter
    def db_instance_identifier(self, value: typing.Optional[str]):
        jsii.set(self, "dbInstanceIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbParameterGroupName")
    def db_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.DBParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbparametergroupname
        """
        return jsii.get(self, "dbParameterGroupName")

    @db_parameter_group_name.setter
    def db_parameter_group_name(self, value: typing.Optional[str]):
        jsii.set(self, "dbParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="dbSnapshotIdentifier")
    def db_snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.DBSnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbsnapshotidentifier
        """
        return jsii.get(self, "dbSnapshotIdentifier")

    @db_snapshot_identifier.setter
    def db_snapshot_identifier(self, value: typing.Optional[str]):
        jsii.set(self, "dbSnapshotIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbsubnetgroupname
        """
        return jsii.get(self, "dbSubnetGroupName")

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[str]):
        jsii.set(self, "dbSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: typing.Optional[str]):
        jsii.set(self, "preferredMaintenanceWindow", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-neptune.CfnDBInstanceProps", jsii_struct_bases=[], name_mapping={'db_instance_class': 'dbInstanceClass', 'allow_major_version_upgrade': 'allowMajorVersionUpgrade', 'auto_minor_version_upgrade': 'autoMinorVersionUpgrade', 'availability_zone': 'availabilityZone', 'db_cluster_identifier': 'dbClusterIdentifier', 'db_instance_identifier': 'dbInstanceIdentifier', 'db_parameter_group_name': 'dbParameterGroupName', 'db_snapshot_identifier': 'dbSnapshotIdentifier', 'db_subnet_group_name': 'dbSubnetGroupName', 'preferred_maintenance_window': 'preferredMaintenanceWindow', 'tags': 'tags'})
class CfnDBInstanceProps():
    def __init__(self, *, db_instance_class: str, allow_major_version_upgrade: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, auto_minor_version_upgrade: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, availability_zone: typing.Optional[str]=None, db_cluster_identifier: typing.Optional[str]=None, db_instance_identifier: typing.Optional[str]=None, db_parameter_group_name: typing.Optional[str]=None, db_snapshot_identifier: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::Neptune::DBInstance``.

        :param db_instance_class: ``AWS::Neptune::DBInstance.DBInstanceClass``.
        :param allow_major_version_upgrade: ``AWS::Neptune::DBInstance.AllowMajorVersionUpgrade``.
        :param auto_minor_version_upgrade: ``AWS::Neptune::DBInstance.AutoMinorVersionUpgrade``.
        :param availability_zone: ``AWS::Neptune::DBInstance.AvailabilityZone``.
        :param db_cluster_identifier: ``AWS::Neptune::DBInstance.DBClusterIdentifier``.
        :param db_instance_identifier: ``AWS::Neptune::DBInstance.DBInstanceIdentifier``.
        :param db_parameter_group_name: ``AWS::Neptune::DBInstance.DBParameterGroupName``.
        :param db_snapshot_identifier: ``AWS::Neptune::DBInstance.DBSnapshotIdentifier``.
        :param db_subnet_group_name: ``AWS::Neptune::DBInstance.DBSubnetGroupName``.
        :param preferred_maintenance_window: ``AWS::Neptune::DBInstance.PreferredMaintenanceWindow``.
        :param tags: ``AWS::Neptune::DBInstance.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html
        """
        self._values = {
            'db_instance_class': db_instance_class,
        }
        if allow_major_version_upgrade is not None: self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if auto_minor_version_upgrade is not None: self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None: self._values["availability_zone"] = availability_zone
        if db_cluster_identifier is not None: self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_instance_identifier is not None: self._values["db_instance_identifier"] = db_instance_identifier
        if db_parameter_group_name is not None: self._values["db_parameter_group_name"] = db_parameter_group_name
        if db_snapshot_identifier is not None: self._values["db_snapshot_identifier"] = db_snapshot_identifier
        if db_subnet_group_name is not None: self._values["db_subnet_group_name"] = db_subnet_group_name
        if preferred_maintenance_window is not None: self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def db_instance_class(self) -> str:
        """``AWS::Neptune::DBInstance.DBInstanceClass``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbinstanceclass
        """
        return self._values.get('db_instance_class')

    @builtins.property
    def allow_major_version_upgrade(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Neptune::DBInstance.AllowMajorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-allowmajorversionupgrade
        """
        return self._values.get('allow_major_version_upgrade')

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Neptune::DBInstance.AutoMinorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-autominorversionupgrade
        """
        return self._values.get('auto_minor_version_upgrade')

    @builtins.property
    def availability_zone(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.AvailabilityZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-availabilityzone
        """
        return self._values.get('availability_zone')

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbclusteridentifier
        """
        return self._values.get('db_cluster_identifier')

    @builtins.property
    def db_instance_identifier(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.DBInstanceIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbinstanceidentifier
        """
        return self._values.get('db_instance_identifier')

    @builtins.property
    def db_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.DBParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbparametergroupname
        """
        return self._values.get('db_parameter_group_name')

    @builtins.property
    def db_snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.DBSnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbsnapshotidentifier
        """
        return self._values.get('db_snapshot_identifier')

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbsubnetgroupname
        """
        return self._values.get('db_subnet_group_name')

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBInstance.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-preferredmaintenancewindow
        """
        return self._values.get('preferred_maintenance_window')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Neptune::DBInstance.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDBInstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDBParameterGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-neptune.CfnDBParameterGroup"):
    """A CloudFormation ``AWS::Neptune::DBParameterGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Neptune::DBParameterGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: str, family: str, parameters: typing.Any, name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::Neptune::DBParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Neptune::DBParameterGroup.Description``.
        :param family: ``AWS::Neptune::DBParameterGroup.Family``.
        :param parameters: ``AWS::Neptune::DBParameterGroup.Parameters``.
        :param name: ``AWS::Neptune::DBParameterGroup.Name``.
        :param tags: ``AWS::Neptune::DBParameterGroup.Tags``.
        """
        props = CfnDBParameterGroupProps(description=description, family=family, parameters=parameters, name=name, tags=tags)

        jsii.create(CfnDBParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any) -> "CfnDBParameterGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Neptune::DBParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::Neptune::DBParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> str:
        """``AWS::Neptune::DBParameterGroup.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-family
        """
        return jsii.get(self, "family")

    @family.setter
    def family(self, value: str):
        jsii.set(self, "family", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        """``AWS::Neptune::DBParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: typing.Any):
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBParameterGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-neptune.CfnDBParameterGroupProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'family': 'family', 'parameters': 'parameters', 'name': 'name', 'tags': 'tags'})
class CfnDBParameterGroupProps():
    def __init__(self, *, description: str, family: str, parameters: typing.Any, name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::Neptune::DBParameterGroup``.

        :param description: ``AWS::Neptune::DBParameterGroup.Description``.
        :param family: ``AWS::Neptune::DBParameterGroup.Family``.
        :param parameters: ``AWS::Neptune::DBParameterGroup.Parameters``.
        :param name: ``AWS::Neptune::DBParameterGroup.Name``.
        :param tags: ``AWS::Neptune::DBParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html
        """
        self._values = {
            'description': description,
            'family': family,
            'parameters': parameters,
        }
        if name is not None: self._values["name"] = name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def description(self) -> str:
        """``AWS::Neptune::DBParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-description
        """
        return self._values.get('description')

    @builtins.property
    def family(self) -> str:
        """``AWS::Neptune::DBParameterGroup.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-family
        """
        return self._values.get('family')

    @builtins.property
    def parameters(self) -> typing.Any:
        """``AWS::Neptune::DBParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-parameters
        """
        return self._values.get('parameters')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBParameterGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-name
        """
        return self._values.get('name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Neptune::DBParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDBParameterGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDBSubnetGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-neptune.CfnDBSubnetGroup"):
    """A CloudFormation ``AWS::Neptune::DBSubnetGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Neptune::DBSubnetGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, db_subnet_group_description: str, subnet_ids: typing.List[str], db_subnet_group_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::Neptune::DBSubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_subnet_group_description: ``AWS::Neptune::DBSubnetGroup.DBSubnetGroupDescription``.
        :param subnet_ids: ``AWS::Neptune::DBSubnetGroup.SubnetIds``.
        :param db_subnet_group_name: ``AWS::Neptune::DBSubnetGroup.DBSubnetGroupName``.
        :param tags: ``AWS::Neptune::DBSubnetGroup.Tags``.
        """
        props = CfnDBSubnetGroupProps(db_subnet_group_description=db_subnet_group_description, subnet_ids=subnet_ids, db_subnet_group_name=db_subnet_group_name, tags=tags)

        jsii.create(CfnDBSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any) -> "CfnDBSubnetGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Neptune::DBSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupDescription")
    def db_subnet_group_description(self) -> str:
        """``AWS::Neptune::DBSubnetGroup.DBSubnetGroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-dbsubnetgroupdescription
        """
        return jsii.get(self, "dbSubnetGroupDescription")

    @db_subnet_group_description.setter
    def db_subnet_group_description(self, value: str):
        jsii.set(self, "dbSubnetGroupDescription", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::Neptune::DBSubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[str]):
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBSubnetGroup.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-dbsubnetgroupname
        """
        return jsii.get(self, "dbSubnetGroupName")

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[str]):
        jsii.set(self, "dbSubnetGroupName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-neptune.CfnDBSubnetGroupProps", jsii_struct_bases=[], name_mapping={'db_subnet_group_description': 'dbSubnetGroupDescription', 'subnet_ids': 'subnetIds', 'db_subnet_group_name': 'dbSubnetGroupName', 'tags': 'tags'})
class CfnDBSubnetGroupProps():
    def __init__(self, *, db_subnet_group_description: str, subnet_ids: typing.List[str], db_subnet_group_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::Neptune::DBSubnetGroup``.

        :param db_subnet_group_description: ``AWS::Neptune::DBSubnetGroup.DBSubnetGroupDescription``.
        :param subnet_ids: ``AWS::Neptune::DBSubnetGroup.SubnetIds``.
        :param db_subnet_group_name: ``AWS::Neptune::DBSubnetGroup.DBSubnetGroupName``.
        :param tags: ``AWS::Neptune::DBSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html
        """
        self._values = {
            'db_subnet_group_description': db_subnet_group_description,
            'subnet_ids': subnet_ids,
        }
        if db_subnet_group_name is not None: self._values["db_subnet_group_name"] = db_subnet_group_name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def db_subnet_group_description(self) -> str:
        """``AWS::Neptune::DBSubnetGroup.DBSubnetGroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-dbsubnetgroupdescription
        """
        return self._values.get('db_subnet_group_description')

    @builtins.property
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::Neptune::DBSubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-subnetids
        """
        return self._values.get('subnet_ids')

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::Neptune::DBSubnetGroup.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-dbsubnetgroupname
        """
        return self._values.get('db_subnet_group_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Neptune::DBSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDBSubnetGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnDBCluster",
    "CfnDBClusterParameterGroup",
    "CfnDBClusterParameterGroupProps",
    "CfnDBClusterProps",
    "CfnDBInstance",
    "CfnDBInstanceProps",
    "CfnDBParameterGroup",
    "CfnDBParameterGroupProps",
    "CfnDBSubnetGroup",
    "CfnDBSubnetGroupProps",
]

publication.publish()
