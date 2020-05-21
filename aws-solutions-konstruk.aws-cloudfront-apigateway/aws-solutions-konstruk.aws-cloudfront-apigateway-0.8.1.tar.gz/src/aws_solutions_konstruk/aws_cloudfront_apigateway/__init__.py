"""
# aws-cloudfront-apigateway module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module.**
>
> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **API Reference**:| <span style="font-weight: normal">http://docs.awssolutionsbuilder.com/aws-solutions-konstruk/latest/api/aws-cloudfront-apigateway/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png){: style="height:16px;width:16px"} Python|`aws_solutions_konstruk.aws_cloudfront_apigateway`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png){: style="height:16px;width:16px"} Typescript|`@aws-solutions-konstruk/aws-cloudfront-apigateway`|

This AWS Solutions Konstruk implements an AWS Cloudfront fronting an Amazon API Gateway REST API.

Here is a minimal deployable pattern definition:

```javascript
const { defaults } = require('@aws-solutions-konstruk/core');
const { CloudFrontToApiGateway } = require('@aws-solutions-konstruk/aws-cloudfront-apigateway');

const stack = new Stack();

const lambdaProps: lambda.FunctionProps = {
    code: lambda.Code.asset(`${__dirname}/lambda`),
    runtime: lambda.Runtime.NODEJS_12_X,
    handler: 'index.handler'
};

const func = defaults.deployLambdaFunction(stack, lambdaProps);

const _api = defaults.RegionalApiGateway(stack, func);

new CloudFrontToApiGateway(stack, 'test-cloudfront-apigateway', {
    existingApiGatewayObj: _api
});

```

## Initializer

```text
new CloudFrontToApiGateway(scope: Construct, id: string, props: CloudFrontToApiGatewayProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`CloudFrontToApiGatewayProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|existingApiGatewayObj|[`api.RestApi`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.RestApi.html)|The regional API Gateway that will be fronted with the CloudFront|
|cloudFrontDistributionProps?|[`cloudfront.CloudFrontWebDistributionProps | any`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudfront.CloudFrontWebDistributionProps.html)|Optional user provided props to override the default props for Cloudfront Distribution|
|insertHttpSecurityHeaders?|`boolean`|Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all resonses from cloudfront|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|cloudFrontWebDistribution()|[`cloudfront.CloudFrontWebDistribution`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudfront.CloudFrontWebDistribution.html)|Returns an instance of cloudfront.CloudFrontWebDistribution created by the construct|
|restApi()|[`api.RestApi`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.RestApi.html)|Returns an instance of the API Gateway REST API created by the pattern.|

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

import aws_cdk.aws_apigateway
import aws_cdk.aws_cloudfront
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.core
import aws_solutions_konstruk.core
import constructs

from ._jsii import *


class CloudFrontToApiGateway(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-konstruk/aws-cloudfront-apigateway.CloudFrontToApiGateway"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, existing_api_gateway_obj: aws_cdk.aws_apigateway.RestApi, cloud_front_distribution_props: typing.Any=None, insert_http_security_headers: typing.Optional[bool]=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param existing_api_gateway_obj: Existing instance of api.RestApi object. Default: - None
        :param cloud_front_distribution_props: Optional user provided props to override the default props. Default: - Default props are used
        :param insert_http_security_headers: Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all resonses from cloudfront. Default: - true

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the CloudFrontToApiGateway class.
        """
        props = CloudFrontToApiGatewayProps(existing_api_gateway_obj=existing_api_gateway_obj, cloud_front_distribution_props=cloud_front_distribution_props, insert_http_security_headers=insert_http_security_headers)

        jsii.create(CloudFrontToApiGateway, self, [scope, id, props])

    @jsii.member(jsii_name="cloudFrontWebDistribution")
    def cloud_front_web_distribution(self) -> aws_cdk.aws_cloudfront.CloudFrontWebDistribution:
        """
        return
        :return: Instance of CloudFrontWebDistribution created by the construct

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Returns an instance of cloudfront.CloudFrontWebDistribution created by the construct.
        """
        return jsii.invoke(self, "cloudFrontWebDistribution", [])

    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> aws_cdk.aws_apigateway.RestApi:
        """
        return
        :return: Instance of RestApi created by the construct

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Returns an instance of api.RestApi created by the construct.
        """
        return jsii.invoke(self, "restApi", [])


@jsii.data_type(jsii_type="@aws-solutions-konstruk/aws-cloudfront-apigateway.CloudFrontToApiGatewayProps", jsii_struct_bases=[], name_mapping={'existing_api_gateway_obj': 'existingApiGatewayObj', 'cloud_front_distribution_props': 'cloudFrontDistributionProps', 'insert_http_security_headers': 'insertHttpSecurityHeaders'})
class CloudFrontToApiGatewayProps():
    def __init__(self, *, existing_api_gateway_obj: aws_cdk.aws_apigateway.RestApi, cloud_front_distribution_props: typing.Any=None, insert_http_security_headers: typing.Optional[bool]=None) -> None:
        """
        :param existing_api_gateway_obj: Existing instance of api.RestApi object. Default: - None
        :param cloud_front_distribution_props: Optional user provided props to override the default props. Default: - Default props are used
        :param insert_http_security_headers: Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all resonses from cloudfront. Default: - true

        summary:
        :summary:: The properties for the CloudFrontToApiGateway Construct
        """
        self._values = {
            'existing_api_gateway_obj': existing_api_gateway_obj,
        }
        if cloud_front_distribution_props is not None: self._values["cloud_front_distribution_props"] = cloud_front_distribution_props
        if insert_http_security_headers is not None: self._values["insert_http_security_headers"] = insert_http_security_headers

    @builtins.property
    def existing_api_gateway_obj(self) -> aws_cdk.aws_apigateway.RestApi:
        """Existing instance of api.RestApi object.

        default
        :default: - None
        """
        return self._values.get('existing_api_gateway_obj')

    @builtins.property
    def cloud_front_distribution_props(self) -> typing.Any:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('cloud_front_distribution_props')

    @builtins.property
    def insert_http_security_headers(self) -> typing.Optional[bool]:
        """Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all resonses from cloudfront.

        default
        :default: - true
        """
        return self._values.get('insert_http_security_headers')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFrontToApiGatewayProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CloudFrontToApiGateway",
    "CloudFrontToApiGatewayProps",
]

publication.publish()
