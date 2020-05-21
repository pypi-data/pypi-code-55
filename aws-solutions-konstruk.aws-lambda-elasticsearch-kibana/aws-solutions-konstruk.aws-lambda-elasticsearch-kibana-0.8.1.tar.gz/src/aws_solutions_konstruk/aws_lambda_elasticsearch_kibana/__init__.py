"""
# aws-lambda-elasticsearch-kibana module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module.**
>
> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **API Reference**:| <span style="font-weight: normal">http://docs.awssolutionsbuilder.com/aws-solutions-konstruk/latest/api/aws-lambda-elasticsearch-kibana/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png){: style="height:16px;width:16px"} Python|`aws_solutions_konstruk.aws_lambda_elasticsearch_kibana`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png){: style="height:16px;width:16px"} Typescript|`@aws-solutions-konstruk/aws-lambda-elasticsearch-kibana`|

This AWS Solutions Konstruk implements the AWS Lambda function and Amazon Elasticsearch Service with the least privileged permissions.

Here is a minimal deployable pattern definition:

```javascript
const { LambdaToElasticSearchAndKibana } = require('@aws-solutions-konstruk/aws-lambda-elasticsearch-kibana');

const lambdaProps: lambda.FunctionProps = {
    code: lambda.Code.asset(`${__dirname}/lambda`),
    runtime: lambda.Runtime.NODEJS_12_X,
    handler: 'index.handler'
};

new LambdaToElasticSearchAndKibana(stack, 'test-lambda-elasticsearch-kibana', {
    lambdaFunctionProps: lambdaProps,
    deployLambda: true,
    domainName: 'test-domain'
});

```

## Initializer

```text
new LambdaToElasticSearchAndKibana(scope: Construct, id: string, props: LambdaToElasticSearchAndKibanaProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`LambdaToElasticSearchAndKibanaProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployLambda|`boolean`|Whether to create a new Lambda function or use an existing Lambda function|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Existing instance of Lambda Function object|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|Optional user provided props to override the default props for Lambda function|
|esDomainProps?|[`elasticsearch.CfnDomainProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-elasticsearch.CfnDomainProps.html)|Optional user provided props to override the default props for the Elasticsearch Service|
|domainName|`string`|Domain name for the Cognito and the Elasticsearch Service|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|lambdaFunction()|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of lambda.Function created by the construct|
|userPool()|[`cognito.UserPool`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.UserPool.html)|Returns an instance of cognito.UserPool created by the construct|
|userPoolClient()|[`cognito.UserPoolClient`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.UserPoolClient.html)|Returns an instance of cognito.UserPoolClient created by the construct|
|identityPool()|[`cognito.CfnIdentityPool`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.CfnIdentityPool.html)|Returns an instance of cognito.CfnIdentityPool created by the construct|
|elasticsearchDomain()|[`elasticsearch.CfnDomain`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-elasticsearch.CfnDomain.html)|Returns an instance of elasticsearch.CfnDomain created by the construct|
|cloudwatchAlarms()|[`cloudwatch.Alarm[]`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudwatch.Alarm.html)|Returns a list of cloudwatch.Alarm created by the construct|

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

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_cognito
import aws_cdk.aws_elasticsearch
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.core
import aws_solutions_konstruk.core
import constructs

from ._jsii import *


class LambdaToElasticSearchAndKibana(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-konstruk/aws-lambda-elasticsearch-kibana.LambdaToElasticSearchAndKibana"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deploy_lambda: bool, domain_name: str, es_domain_props: typing.Optional[aws_cdk.aws_elasticsearch.CfnDomainProps]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide a lambda function object as ``existingLambdaObj`` Default: - true
        :param domain_name: Cognito & ES Domain Name. Default: - None
        :param es_domain_props: Optional user provided props to override the default props for the Elasticsearch Service. Default: - Default props are used
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided props to override the default props for the Lambda function. If ``deploy`` is set to true only then this property is required Default: - Default props are used

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the CognitoToApiGatewayToLambda class.
        """
        props = LambdaToElasticSearchAndKibanaProps(deploy_lambda=deploy_lambda, domain_name=domain_name, es_domain_props=es_domain_props, existing_lambda_obj=existing_lambda_obj, lambda_function_props=lambda_function_props)

        jsii.create(LambdaToElasticSearchAndKibana, self, [scope, id, props])

    @jsii.member(jsii_name="cloudwatchAlarms")
    def cloudwatch_alarms(self) -> typing.List[aws_cdk.aws_cloudwatch.Alarm]:
        """
        return
        :return: List of cloudwatch.Alarm  created by the construct

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Returns a list of cloudwatch.Alarm created by the construct.
        """
        return jsii.invoke(self, "cloudwatchAlarms", [])

    @jsii.member(jsii_name="elasticsearchDomain")
    def elasticsearch_domain(self) -> aws_cdk.aws_elasticsearch.CfnDomain:
        """
        return
        :return: Instance of CfnDomain created by the construct

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Returns an instance of elasticsearch.CfnDomain created by the construct.
        """
        return jsii.invoke(self, "elasticsearchDomain", [])

    @jsii.member(jsii_name="identityPool")
    def identity_pool(self) -> aws_cdk.aws_cognito.CfnIdentityPool:
        """
        return
        :return: Instance of CfnIdentityPool created by the construct

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Returns an instance of cognito.CfnIdentityPool created by the construct.
        """
        return jsii.invoke(self, "identityPool", [])

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

    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> aws_cdk.aws_cognito.UserPool:
        """
        return
        :return: Instance of UserPool created by the construct

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Returns an instance of cognito.UserPool created by the construct.
        """
        return jsii.invoke(self, "userPool", [])

    @jsii.member(jsii_name="userPoolClient")
    def user_pool_client(self) -> aws_cdk.aws_cognito.UserPoolClient:
        """
        return
        :return: Instance of UserPoolClient created by the construct

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Returns an instance of cognito.UserPoolClient created by the construct.
        """
        return jsii.invoke(self, "userPoolClient", [])


@jsii.data_type(jsii_type="@aws-solutions-konstruk/aws-lambda-elasticsearch-kibana.LambdaToElasticSearchAndKibanaProps", jsii_struct_bases=[], name_mapping={'deploy_lambda': 'deployLambda', 'domain_name': 'domainName', 'es_domain_props': 'esDomainProps', 'existing_lambda_obj': 'existingLambdaObj', 'lambda_function_props': 'lambdaFunctionProps'})
class LambdaToElasticSearchAndKibanaProps():
    def __init__(self, *, deploy_lambda: bool, domain_name: str, es_domain_props: typing.Optional[aws_cdk.aws_elasticsearch.CfnDomainProps]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide a lambda function object as ``existingLambdaObj`` Default: - true
        :param domain_name: Cognito & ES Domain Name. Default: - None
        :param es_domain_props: Optional user provided props to override the default props for the Elasticsearch Service. Default: - Default props are used
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided props to override the default props for the Lambda function. If ``deploy`` is set to true only then this property is required Default: - Default props are used

        summary:
        :summary:: The properties for the CognitoToApiGatewayToLambda Construct
        """
        if isinstance(es_domain_props, dict): es_domain_props = aws_cdk.aws_elasticsearch.CfnDomainProps(**es_domain_props)
        if isinstance(lambda_function_props, dict): lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        self._values = {
            'deploy_lambda': deploy_lambda,
            'domain_name': domain_name,
        }
        if es_domain_props is not None: self._values["es_domain_props"] = es_domain_props
        if existing_lambda_obj is not None: self._values["existing_lambda_obj"] = existing_lambda_obj
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
    def domain_name(self) -> str:
        """Cognito & ES Domain Name.

        default
        :default: - None
        """
        return self._values.get('domain_name')

    @builtins.property
    def es_domain_props(self) -> typing.Optional[aws_cdk.aws_elasticsearch.CfnDomainProps]:
        """Optional user provided props to override the default props for the Elasticsearch Service.

        default
        :default: - Default props are used
        """
        return self._values.get('es_domain_props')

    @builtins.property
    def existing_lambda_obj(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        """Existing instance of Lambda Function object.

        If ``deploy`` is set to false only then this property is required

        default
        :default: - None
        """
        return self._values.get('existing_lambda_obj')

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
        return 'LambdaToElasticSearchAndKibanaProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "LambdaToElasticSearchAndKibana",
    "LambdaToElasticSearchAndKibanaProps",
]

publication.publish()
