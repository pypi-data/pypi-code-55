"""
# Include CloudFormation templates in the CDK

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module contains a set of classes whose goal is to facilitate working
with existing CloudFormation templates in the CDK.
It can be thought of as an extension of the capabilities of the
[`CfnInclude` class](../@aws-cdk/core/lib/cfn-include.ts).

## Basic usage

Assume we have a file `my-template.json`, that contains the following CloudFormation template:

```json
{
  "Resources": {
    "Bucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": "some-bucket-name"
      }
    }
  }
}
```

It can be included in a CDK application with the following code:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.cloudformation_include as cfn_inc

cfn_template = cfn_inc.CfnInclude(self, "Template",
    template_file="my-template.json"
)
```

This will add all resources from `my-template.json` into the CDK application,
preserving their original logical IDs from the template file.

Any resource from the included template can be retrieved by referring to it by its logical ID from the template.
If you know the class of the CDK object that corresponds to that resource,
you can cast the returned object to the correct type:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_s3 as s3

cfn_bucket = cfn_template.get_resource("Bucket")
```

Any modifications made to that resource will be reflected in the resulting CDK template;
for example, the name of the bucket can be changed:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_bucket.bucket_name = "my-bucket-name"
```

You can also refer to the resource when defining other constructs,
including the higher-level ones
(those whose name does not start with `Cfn`),
for example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iam as iam

role = iam.Role(self, "Role",
    assumed_by=iam.AnyPrincipal()
)
role.add_to_policy(iam.PolicyStatement(
    actions=["s3:*"],
    resources=[cfn_bucket.attr_arn]
))
```

If you need, you can also convert the CloudFormation resource to a higher-level
resource by importing it by its name:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = s3.Bucket.from_bucket_name(self, "L2Bucket", cfn_bucket.ref)
```

## Known limitations

This module is still in its early, experimental stage,
and so does not implement all features of CloudFormation templates.
All items unchecked below are currently not supported.

### Ability to retrieve CloudFormation objects from the template:

* [x] Resources
* [ ] Parameters
* [ ] Conditions
* [ ] Outputs

### [Resource attributes](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-product-attribute-reference.html):

* [x] Properties
* [ ] Condition
* [x] DependsOn
* [ ] CreationPolicy
* [ ] UpdatePolicy
* [x] UpdateReplacePolicy
* [x] DeletionPolicy
* [x] Metadata

### [CloudFormation functions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html):

* [x] Ref
* [x] Fn::GetAtt
* [x] Fn::Join
* [x] Fn::If
* [ ] Fn::And
* [ ] Fn::Equals
* [ ] Fn::Not
* [ ] Fn::Or
* [ ] Fn::Base64
* [ ] Fn::Cidr
* [ ] Fn::FindInMap
* [ ] Fn::GetAZs
* [ ] Fn::ImportValue
* [ ] Fn::Select
* [ ] Fn::Split
* [ ] Fn::Sub
* [ ] Fn::Transform
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.alexa_ask
import aws_cdk.aws_accessanalyzer
import aws_cdk.aws_acmpca
import aws_cdk.aws_amazonmq
import aws_cdk.aws_amplify
import aws_cdk.aws_apigateway
import aws_cdk.aws_apigatewayv2
import aws_cdk.aws_appconfig
import aws_cdk.aws_applicationautoscaling
import aws_cdk.aws_appmesh
import aws_cdk.aws_appstream
import aws_cdk.aws_appsync
import aws_cdk.aws_athena
import aws_cdk.aws_autoscaling
import aws_cdk.aws_autoscalingplans
import aws_cdk.aws_backup
import aws_cdk.aws_batch
import aws_cdk.aws_budgets
import aws_cdk.aws_cassandra
import aws_cdk.aws_ce
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_chatbot
import aws_cdk.aws_cloud9
import aws_cdk.aws_cloudfront
import aws_cdk.aws_cloudtrail
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_codebuild
import aws_cdk.aws_codecommit
import aws_cdk.aws_codedeploy
import aws_cdk.aws_codeguruprofiler
import aws_cdk.aws_codepipeline
import aws_cdk.aws_codestar
import aws_cdk.aws_codestarconnections
import aws_cdk.aws_codestarnotifications
import aws_cdk.aws_cognito
import aws_cdk.aws_config
import aws_cdk.aws_datapipeline
import aws_cdk.aws_dax
import aws_cdk.aws_detective
import aws_cdk.aws_directoryservice
import aws_cdk.aws_dlm
import aws_cdk.aws_dms
import aws_cdk.aws_docdb
import aws_cdk.aws_dynamodb
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_ecs
import aws_cdk.aws_efs
import aws_cdk.aws_eks
import aws_cdk.aws_elasticache
import aws_cdk.aws_elasticbeanstalk
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_elasticsearch
import aws_cdk.aws_emr
import aws_cdk.aws_events
import aws_cdk.aws_eventschemas
import aws_cdk.aws_fms
import aws_cdk.aws_fsx
import aws_cdk.aws_gamelift
import aws_cdk.aws_globalaccelerator
import aws_cdk.aws_glue
import aws_cdk.aws_greengrass
import aws_cdk.aws_guardduty
import aws_cdk.aws_iam
import aws_cdk.aws_imagebuilder
import aws_cdk.aws_inspector
import aws_cdk.aws_iot
import aws_cdk.aws_iot1click
import aws_cdk.aws_iotanalytics
import aws_cdk.aws_iotevents
import aws_cdk.aws_iotthingsgraph
import aws_cdk.aws_kinesis
import aws_cdk.aws_kinesisanalytics
import aws_cdk.aws_kinesisfirehose
import aws_cdk.aws_kms
import aws_cdk.aws_lakeformation
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_macie
import aws_cdk.aws_managedblockchain
import aws_cdk.aws_mediaconvert
import aws_cdk.aws_medialive
import aws_cdk.aws_mediastore
import aws_cdk.aws_msk
import aws_cdk.aws_neptune
import aws_cdk.aws_networkmanager
import aws_cdk.aws_opsworks
import aws_cdk.aws_opsworkscm
import aws_cdk.aws_pinpoint
import aws_cdk.aws_pinpointemail
import aws_cdk.aws_qldb
import aws_cdk.aws_ram
import aws_cdk.aws_rds
import aws_cdk.aws_redshift
import aws_cdk.aws_resourcegroups
import aws_cdk.aws_robomaker
import aws_cdk.aws_route53
import aws_cdk.aws_route53resolver
import aws_cdk.aws_s3
import aws_cdk.aws_sagemaker
import aws_cdk.aws_sam
import aws_cdk.aws_sdb
import aws_cdk.aws_secretsmanager
import aws_cdk.aws_securityhub
import aws_cdk.aws_servicecatalog
import aws_cdk.aws_servicediscovery
import aws_cdk.aws_ses
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.aws_ssm
import aws_cdk.aws_stepfunctions
import aws_cdk.aws_synthetics
import aws_cdk.aws_transfer
import aws_cdk.aws_waf
import aws_cdk.aws_wafregional
import aws_cdk.aws_wafv2
import aws_cdk.aws_workspaces
import aws_cdk.core
import constructs

from ._jsii import *


class CfnInclude(aws_cdk.core.CfnElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cloudformation-include.CfnInclude"):
    """Construct to import an existing CloudFormation template file into a CDK application.

    All resources defined in the template file can be retrieved by calling the {@link getResource} method.
    Any modifications made on the returned resource objects will be reflected in the resulting CDK template.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, template_file: str) -> None:
        """
        :param scope: -
        :param id: -
        :param template_file: Path to the template file. Currently, only JSON templates are supported.

        stability
        :stability: experimental
        """
        props = CfnIncludeProps(template_file=template_file)

        jsii.create(CfnInclude, self, [scope, id, props])

    @jsii.member(jsii_name="getResource")
    def get_resource(self, logical_id: str) -> aws_cdk.core.CfnResource:
        """Returns the low-level CfnResource from the template with the given logical ID.

        Any modifications performed on that resource will be reflected in the resulting CDK template.

        The returned object will be of the proper underlying class;
        you can always cast it to the correct type in your code::

            // assume the template contains an AWS::S3::Bucket with logical ID 'Bucket'
            const cfnBucket = cfnTemplate.getResource('Bucket') as s3.CfnBucket;
            // cfnBucket is of type s3.CfnBucket

        If the template does not contain a resource with the given logical ID,
        an exception will be thrown.

        :param logical_id: the logical ID of the resource in the CloudFormation template file.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getResource", [logical_id])


@jsii.data_type(jsii_type="@aws-cdk/cloudformation-include.CfnIncludeProps", jsii_struct_bases=[], name_mapping={'template_file': 'templateFile'})
class CfnIncludeProps():
    def __init__(self, *, template_file: str) -> None:
        """Construction properties of {@link CfnInclude}.

        :param template_file: Path to the template file. Currently, only JSON templates are supported.

        stability
        :stability: experimental
        """
        self._values = {
            'template_file': template_file,
        }

    @builtins.property
    def template_file(self) -> str:
        """Path to the template file.

        Currently, only JSON templates are supported.

        stability
        :stability: experimental
        """
        return self._values.get('template_file')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIncludeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnInclude",
    "CfnIncludeProps",
]

publication.publish()
