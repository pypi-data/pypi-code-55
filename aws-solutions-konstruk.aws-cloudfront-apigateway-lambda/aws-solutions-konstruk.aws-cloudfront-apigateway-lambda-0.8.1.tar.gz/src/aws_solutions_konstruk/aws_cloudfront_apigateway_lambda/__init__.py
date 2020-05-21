"""
# aws-cloudfront-apigateway-lambda module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module.**
>
> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **API Reference**:| <span style="font-weight: normal">http://docs.awssolutionsbuilder.com/aws-solutions-konstruk/latest/api/aws-cloudfront-apigateway-lambda/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png){: style="height:16px;width:16px"} Python|`aws_solutions_konstruk.aws_cloudfront_apigateway_lambda`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png){: style="height:16px;width:16px"} Typescript|`@aws-solutions-konstruk/aws-cloudfront-apigateway-lambda`|

This AWS Solutions Konstruk implements an AWS Cloudfront fronting an Amazon API Gateway Lambda backed REST API.

Here is a minimal deployable pattern definition:

```javascript
import * as defaults from '@aws-solutions-konstruk/core';
import { CloudFrontToApiGatewayToLambda } from '@aws-solutions-konstruk/aws-cloudfront-apigateway-lambda';

const stack = new Stack();

const lambdaProps: lambda.FunctionProps = {
    code: lambda.Code.asset(`${__dirname}/lambda`),
    runtime: lambda.Runtime.NODEJS_12_X,
    handler: 'index.handler'
};

new CloudFrontToApiGatewayToLambda(stack, 'test-cloudfront-apigateway-lambda', {
    lambdaFunctionProps: lambdaProps,
    deployLambda: true
});
```

## Initializer

```text
new CloudFrontToApiGatewayToLambda(scope: Construct, id: string, props: CloudFrontToApiGatewayToLambdaProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`CloudFrontToApiGatewayToLambdaProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployLambda|`boolean`|Whether to create a new Lambda function or use an existing Lambda function|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Existing instance of Lambda Function object|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|Optional user provided props to override the default props for Lambda function|
|apiGatewayProps?|[`api.LambdaRestApiProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.LambdaRestApiProps.html)|Optional user provided props to override the default props for API Gateway|
|cloudFrontDistributionProps?|[`cloudfront.CloudFrontWebDistributionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudfront.CloudFrontWebDistributionProps.html)|Optional user provided props to override the default props for Cloudfront Distribution|
|insertHttpSecurityHeaders?|`boolean`|Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all resonses from cloudfront|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|cloudFrontWebDistribution()|[`cloudfront.CloudFrontWebDistribution`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudfront.CloudFrontWebDistribution.html)|Returns an instance of cloudfront.CloudFrontWebDistribution created by the construct|
|lambdaFunction()|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of the Lambda function created by the pattern.|
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
import aws_solutions_konstruk.aws_cloudfront_apigateway
import aws_solutions_konstruk.core
import constructs

from ._jsii import *


class CloudFrontToApiGatewayToLambda(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-konstruk/aws-cloudfront-apigateway-lambda.CloudFrontToApiGatewayToLambda"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deploy_lambda: bool, api_gateway_props: typing.Optional[aws_cdk.aws_apigateway.LambdaRestApiProps]=None, cloud_front_distribution_props: typing.Any=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, insert_http_security_headers: typing.Optional[bool]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide a lambda function object as ``existingLambdaObj`` Default: - true
        :param api_gateway_props: Optional user provided props to override the default props for the API Gateway. Default: - Default props are used
        :param cloud_front_distribution_props: Optional user provided props to override the default props. Default: - Default props are used
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param insert_http_security_headers: Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all resonses from cloudfront. Default: - true
        :param lambda_function_props: Optional user provided props to override the default props for the Lambda function. If ``deploy`` is set to true only then this property is required Default: - Default props are used

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the CloudFrontToApiGatewayToLambda class.
        """
        props = CloudFrontToApiGatewayToLambdaProps(deploy_lambda=deploy_lambda, api_gateway_props=api_gateway_props, cloud_front_distribution_props=cloud_front_distribution_props, existing_lambda_obj=existing_lambda_obj, insert_http_security_headers=insert_http_security_headers, lambda_function_props=lambda_function_props)

        jsii.create(CloudFrontToApiGatewayToLambda, self, [scope, id, props])

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

    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        """
        return
        :return: Instance of Function created by the construct

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Returns an instance of lambda.Function created by the construct.
        """
        return jsii.invoke(self, "lambdaFunction", [])

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


@jsii.data_type(jsii_type="@aws-solutions-konstruk/aws-cloudfront-apigateway-lambda.CloudFrontToApiGatewayToLambdaProps", jsii_struct_bases=[], name_mapping={'deploy_lambda': 'deployLambda', 'api_gateway_props': 'apiGatewayProps', 'cloud_front_distribution_props': 'cloudFrontDistributionProps', 'existing_lambda_obj': 'existingLambdaObj', 'insert_http_security_headers': 'insertHttpSecurityHeaders', 'lambda_function_props': 'lambdaFunctionProps'})
class CloudFrontToApiGatewayToLambdaProps():
    def __init__(self, *, deploy_lambda: bool, api_gateway_props: typing.Optional[aws_cdk.aws_apigateway.LambdaRestApiProps]=None, cloud_front_distribution_props: typing.Any=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, insert_http_security_headers: typing.Optional[bool]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide a lambda function object as ``existingLambdaObj`` Default: - true
        :param api_gateway_props: Optional user provided props to override the default props for the API Gateway. Default: - Default props are used
        :param cloud_front_distribution_props: Optional user provided props to override the default props. Default: - Default props are used
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param insert_http_security_headers: Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all resonses from cloudfront. Default: - true
        :param lambda_function_props: Optional user provided props to override the default props for the Lambda function. If ``deploy`` is set to true only then this property is required Default: - Default props are used

        summary:
        :summary:: The properties for the CloudFrontToApiGatewayToLambda Construct
        """
        if isinstance(api_gateway_props, dict): api_gateway_props = aws_cdk.aws_apigateway.LambdaRestApiProps(**api_gateway_props)
        if isinstance(lambda_function_props, dict): lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        self._values = {
            'deploy_lambda': deploy_lambda,
        }
        if api_gateway_props is not None: self._values["api_gateway_props"] = api_gateway_props
        if cloud_front_distribution_props is not None: self._values["cloud_front_distribution_props"] = cloud_front_distribution_props
        if existing_lambda_obj is not None: self._values["existing_lambda_obj"] = existing_lambda_obj
        if insert_http_security_headers is not None: self._values["insert_http_security_headers"] = insert_http_security_headers
        if lambda_function_props is not None: self._values["lambda_function_props"] = lambda_function_props

    @builtins.property
    def deploy_lambda(self) -> bool:
        """Whether to create a new Lambda function or use an existing Lambda function.

        If set to false, you must provide a lambda function object as ``existingLambdaObj``

        default
        :default: - true
        """
        return self._values.get('deploy_lambda')

    @builtins.property
    def api_gateway_props(self) -> typing.Optional[aws_cdk.aws_apigateway.LambdaRestApiProps]:
        """Optional user provided props to override the default props for the API Gateway.

        default
        :default: - Default props are used
        """
        return self._values.get('api_gateway_props')

    @builtins.property
    def cloud_front_distribution_props(self) -> typing.Any:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('cloud_front_distribution_props')

    @builtins.property
    def existing_lambda_obj(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        """Existing instance of Lambda Function object.

        If ``deploy`` is set to false only then this property is required

        default
        :default: - None
        """
        return self._values.get('existing_lambda_obj')

    @builtins.property
    def insert_http_security_headers(self) -> typing.Optional[bool]:
        """Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all resonses from cloudfront.

        default
        :default: - true
        """
        return self._values.get('insert_http_security_headers')

    @builtins.property
    def lambda_function_props(self) -> typing.Optional[aws_cdk.aws_lambda.FunctionProps]:
        """Optional user provided props to override the default props for the Lambda function.

        If ``deploy`` is set to true only then this property is required

        default
        :default: - Default props are used
        """
        return self._values.get('lambda_function_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFrontToApiGatewayToLambdaProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CloudFrontToApiGatewayToLambda",
    "CloudFrontToApiGatewayToLambdaProps",
]

publication.publish()
