"""
# aws-kinesisfirehose-s3 module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module.**
>
> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **API Reference**:| <span style="font-weight: normal">http://docs.awssolutionsbuilder.com/aws-solutions-konstruk/latest/api/aws-kinesisfirehose-s3/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png){: style="height:16px;width:16px"} Python|`aws_solutions_konstruk.aws_kinesisfirehose_s3`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png){: style="height:16px;width:16px"} Typescript|`@aws-solutions-konstruk/aws-kinesisfirehose-s3`|

This AWS Solutions Konstruk implements an Amazon Kinesis Data Firehose delivery stream connected to an Amazon S3 bucket.

Here is a minimal deployable pattern definition:

```javascript
const { KinesisFirehoseToS3 } = require('@aws-solutions-konstruk/aws-kinesisfirehose-s3');

new KinesisFirehoseToS3(stack, 'test-firehose-s3', {});

```

## Initializer

```text
new KinesisFirehoseToS3(scope: Construct, id: string, props: KinesisFirehoseToS3Props);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`KinesisFirehoseToS3Props`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|kinesisFirehoseProps?|[`kinesisfirehose.CfnDeliveryStreamProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesisfirehose.CfnDeliveryStreamProps.html)|Optional user provided props to override the default props for Kinesis Firehose Delivery Stream|
|deployBucket?|`boolean`|Whether to create a S3 Bucket or use an existing S3 Bucket|
|existingBucketObj?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Existing instance of S3 Bucket object|
|bucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.BucketProps.html)|Optional user provided props to override the default props for S3 Bucket|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|kinesisFirehose()|[`kinesisfirehose.CfnDeliveryStream`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesisfirehose.CfnDeliveryStream.html)|Returns an instance of kinesisfirehose.CfnDeliveryStream created by the construct|
|bucket()|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Returns an instance of s3.Bucket created by the construct|

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_iam
import aws_cdk.aws_kinesisfirehose
import aws_cdk.aws_logs
import aws_cdk.aws_s3
import aws_cdk.core
import aws_solutions_konstruk.core
import constructs

from ._jsii import *


class KinesisFirehoseToS3(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-konstruk/aws-kinesisfirehose-s3.KinesisFirehoseToS3"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None, kinesis_firehose_props: typing.Any=None) -> None:
        """Constructs a new instance of the IotToLambda class.

        :param scope: -
        :param id: -
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        :param kinesis_firehose_props: Optional user provided props to override the default props. Default: - Default props are used
        """
        props = KinesisFirehoseToS3Props(bucket_props=bucket_props, deploy_bucket=deploy_bucket, existing_bucket_obj=existing_bucket_obj, kinesis_firehose_props=kinesis_firehose_props)

        jsii.create(KinesisFirehoseToS3, self, [scope, id, props])

    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.Bucket:
        """Returns an instance of s3.Bucket created by the construct."""
        return jsii.invoke(self, "bucket", [])

    @jsii.member(jsii_name="kinesisFirehose")
    def kinesis_firehose(self) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream:
        """Returns an instance of kinesisfirehose.CfnDeliveryStream created by the construct."""
        return jsii.invoke(self, "kinesisFirehose", [])


@jsii.data_type(jsii_type="@aws-solutions-konstruk/aws-kinesisfirehose-s3.KinesisFirehoseToS3Props", jsii_struct_bases=[], name_mapping={'bucket_props': 'bucketProps', 'deploy_bucket': 'deployBucket', 'existing_bucket_obj': 'existingBucketObj', 'kinesis_firehose_props': 'kinesisFirehoseProps'})
class KinesisFirehoseToS3Props():
    def __init__(self, *, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None, kinesis_firehose_props: typing.Any=None) -> None:
        """The properties for the KinesisFirehoseToS3 class.

        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        :param kinesis_firehose_props: Optional user provided props to override the default props. Default: - Default props are used
        """
        if isinstance(bucket_props, dict): bucket_props = aws_cdk.aws_s3.BucketProps(**bucket_props)
        self._values = {
        }
        if bucket_props is not None: self._values["bucket_props"] = bucket_props
        if deploy_bucket is not None: self._values["deploy_bucket"] = deploy_bucket
        if existing_bucket_obj is not None: self._values["existing_bucket_obj"] = existing_bucket_obj
        if kinesis_firehose_props is not None: self._values["kinesis_firehose_props"] = kinesis_firehose_props

    @builtins.property
    def bucket_props(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        """Optional user provided props to override the default props.

        If ``deploy`` is set to true only then this property is required

        default
        :default: - Default props are used
        """
        return self._values.get('bucket_props')

    @builtins.property
    def deploy_bucket(self) -> typing.Optional[bool]:
        """Whether to create a S3 Bucket or use an existing S3 Bucket.

        If set to false, you must provide S3 Bucket as ``existingBucketObj``

        default
        :default: - true
        """
        return self._values.get('deploy_bucket')

    @builtins.property
    def existing_bucket_obj(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        """Existing instance of S3 Bucket object.

        If ``deployBucket`` is set to false only then this property is required

        default
        :default: - None
        """
        return self._values.get('existing_bucket_obj')

    @builtins.property
    def kinesis_firehose_props(self) -> typing.Any:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('kinesis_firehose_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'KinesisFirehoseToS3Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "KinesisFirehoseToS3",
    "KinesisFirehoseToS3Props",
]

publication.publish()
