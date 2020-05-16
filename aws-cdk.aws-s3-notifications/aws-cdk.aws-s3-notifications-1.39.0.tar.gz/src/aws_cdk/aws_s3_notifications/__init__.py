"""
## S3 Bucket Notifications Destinations

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module includes integration classes for using Topics, Queues or Lambdas
as S3 Notification Destinations.

## Example

The following example shows how to send a notification to an SNS
topic when an object is created in an S3 bucket:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_s3_notifications as s3n

bucket = s3.Bucket(stack, "Bucket")
topic = sns.Topic(stack, "Topic")

bucket.add_event_notification(s3.EventType.OBJECT_CREATED_PUT, s3n.SnsDestination(topic))
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

import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.core
import constructs

from ._jsii import *


@jsii.implements(aws_cdk.aws_s3.IBucketNotificationDestination)
class LambdaDestination(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-notifications.LambdaDestination"):
    """Use a Lambda function as a bucket notification destination."""
    def __init__(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        """
        :param fn: -
        """
        jsii.create(LambdaDestination, self, [fn])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, bucket: aws_cdk.aws_s3.IBucket) -> aws_cdk.aws_s3.BucketNotificationDestinationConfig:
        """Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param _scope: -
        :param bucket: -
        """
        return jsii.invoke(self, "bind", [_scope, bucket])


@jsii.implements(aws_cdk.aws_s3.IBucketNotificationDestination)
class SnsDestination(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-notifications.SnsDestination"):
    """Use an SNS topic as a bucket notification destination."""
    def __init__(self, topic: aws_cdk.aws_sns.ITopic) -> None:
        """
        :param topic: -
        """
        jsii.create(SnsDestination, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, bucket: aws_cdk.aws_s3.IBucket) -> aws_cdk.aws_s3.BucketNotificationDestinationConfig:
        """Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param _scope: -
        :param bucket: -
        """
        return jsii.invoke(self, "bind", [_scope, bucket])


@jsii.implements(aws_cdk.aws_s3.IBucketNotificationDestination)
class SqsDestination(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-notifications.SqsDestination"):
    """Use an SQS queue as a bucket notification destination."""
    def __init__(self, queue: aws_cdk.aws_sqs.IQueue) -> None:
        """
        :param queue: -
        """
        jsii.create(SqsDestination, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: aws_cdk.core.Construct, bucket: aws_cdk.aws_s3.IBucket) -> aws_cdk.aws_s3.BucketNotificationDestinationConfig:
        """Allows using SQS queues as destinations for bucket notifications.

        Use ``bucket.onEvent(event, queue)`` to subscribe.

        :param _scope: -
        :param bucket: -
        """
        return jsii.invoke(self, "bind", [_scope, bucket])


__all__ = [
    "LambdaDestination",
    "SnsDestination",
    "SqsDestination",
]

publication.publish()
