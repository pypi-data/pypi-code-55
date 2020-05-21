"""
# aws-events-rule-lambda module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module.**
>
> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **API Reference**:| <span style="font-weight: normal">http://docs.awssolutionsbuilder.com/aws-solutions-konstruk/latest/api/aws-events-rule-lambda/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png){: style="height:16px;width:16px"} Python|`aws_solutions_konstruk.aws_events_rule_lambda`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png){: style="height:16px;width:16px"} Typescript|`@aws-solutions-konstruk/aws-events-rule-lambda`|

This AWS Solutions Konstruk implements an AWS Events rule and an AWS Lambda function.

Here is a minimal deployable pattern definition:

```javascript
const { EventsRuleToLambdaProps, EventsRuleToLambda } = require('@aws-solutions-konstruk/aws-events-rule-lambda');

const props: EventsRuleToLambdaProps = {
    deployLambda: true,
    lambdaFunctionProps: {
        code: lambda.Code.asset(`${__dirname}/lambda`),
        runtime: lambda.Runtime.NODEJS_12_X,
        handler: 'index.handler'
    },
    eventRuleProps: {
      schedule: events.Schedule.rate(Duration.minutes(5))
    }
};

new EventsRuleToLambda(stack, 'test-events-rule-lambda', props);
```

## Initializer

```text
new EventsRuleToLambda(scope: Construct, id: string, props: EventsRuleToLambdaProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`EventsRuleToLambdaProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployLambda|`boolean`|Whether to create a new lambda function or use an existing lambda function|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Existing instance of Lambda Function object|
|lambdaFunctionProps|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|Optional user provided props to override the default props for lambda.Function|
|eventRuleProps|[`events.RuleProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.RuleProps.html)|User provided eventRuleProps to override the defaults|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|eventsRule()|[`events.Rule`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.Rule.html)|Returns an instance of events.Rule created by the construct|
|lambdaFunction()|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of lambda.Function created by the construct|

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

import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.core
import aws_solutions_konstruk.core
import constructs

from ._jsii import *


class EventsRuleToLambda(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-konstruk/aws-events-rule-lambda.EventsRuleToLambda"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deploy_lambda: bool, event_rule_props: aws_cdk.aws_events.RuleProps, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param deploy_lambda: Whether to create a new lambda function or use an existing lambda function. If set to false, you must provide a lambda function object as ``existingObj`` Default: - true
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the EventsRuleToLambda class.
        """
        props = EventsRuleToLambdaProps(deploy_lambda=deploy_lambda, event_rule_props=event_rule_props, existing_lambda_obj=existing_lambda_obj, lambda_function_props=lambda_function_props)

        jsii.create(EventsRuleToLambda, self, [scope, id, props])

    @jsii.member(jsii_name="eventsRule")
    def events_rule(self) -> aws_cdk.aws_events.Rule:
        """
        return
        :return: Instance of events.Rule created by the construct

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Returns an instance of events.Rule created by the construct.
        """
        return jsii.invoke(self, "eventsRule", [])

    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        """
        return
        :return: Instance of lambda.Function created by the construct

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Returns an instance of lambda.Function created by the construct.
        """
        return jsii.invoke(self, "lambdaFunction", [])


@jsii.data_type(jsii_type="@aws-solutions-konstruk/aws-events-rule-lambda.EventsRuleToLambdaProps", jsii_struct_bases=[], name_mapping={'deploy_lambda': 'deployLambda', 'event_rule_props': 'eventRuleProps', 'existing_lambda_obj': 'existingLambdaObj', 'lambda_function_props': 'lambdaFunctionProps'})
class EventsRuleToLambdaProps():
    def __init__(self, *, deploy_lambda: bool, event_rule_props: aws_cdk.aws_events.RuleProps, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param deploy_lambda: Whether to create a new lambda function or use an existing lambda function. If set to false, you must provide a lambda function object as ``existingObj`` Default: - true
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used

        summary:
        :summary:: The properties for the CloudFrontToApiGateway Construct
        """
        if isinstance(event_rule_props, dict): event_rule_props = aws_cdk.aws_events.RuleProps(**event_rule_props)
        if isinstance(lambda_function_props, dict): lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        self._values = {
            'deploy_lambda': deploy_lambda,
            'event_rule_props': event_rule_props,
        }
        if existing_lambda_obj is not None: self._values["existing_lambda_obj"] = existing_lambda_obj
        if lambda_function_props is not None: self._values["lambda_function_props"] = lambda_function_props

    @builtins.property
    def deploy_lambda(self) -> bool:
        """Whether to create a new lambda function or use an existing lambda function.

        If set to false, you must provide a lambda function object as ``existingObj``

        default
        :default: - true
        """
        return self._values.get('deploy_lambda')

    @builtins.property
    def event_rule_props(self) -> aws_cdk.aws_events.RuleProps:
        """User provided eventRuleProps to override the defaults.

        default
        :default: - None
        """
        return self._values.get('event_rule_props')

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
        """Optional user provided props to override the default props.

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
        return 'EventsRuleToLambdaProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "EventsRuleToLambda",
    "EventsRuleToLambdaProps",
]

publication.publish()
