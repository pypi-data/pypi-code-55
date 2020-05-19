"""
# CDK Apex Cname - Route53

A CDK utility construct to allowing setting an domain apex (in Route53) to resolve to a cname record of a resource
not in Route 53.

## Usage

### Typescript

First install the package

```
npm install cdk-apex-cname
```

Then you can use the Apex CNAME in your code:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_apex_cname import CdkApexCname

CdkApexCname(self, "CdkApexCname",
    apex_name="apex.com",
    record_name="cname.example.com",
    hosted_zone_id="ZONE1234",
    apex_cname_rule_cron="cron(0 * ? * * *)"
)
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

import aws_cdk.aws_events
import aws_cdk.aws_events_targets
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.core
import constructs

__jsii_assembly__ = jsii.JSIIAssembly.load("cdk-apex-cname", "0.1.4", __name__, "cdk-apex-cname@0.1.4.jsii.tgz")


class CdkApexCname(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-apex-cname.CdkApexCname"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, apex_cname_rule_cron: str, apex_name: str, hosted_zone_id: str, record_name: str) -> None:
        """
        :param scope: -
        :param id: -
        :param apex_cname_rule_cron: -
        :param apex_name: The properties for the Apex Cname Lambda.
        :param hosted_zone_id: -
        :param record_name: -
        """
        props = CdkApexCnameProps(apex_cname_rule_cron=apex_cname_rule_cron, apex_name=apex_name, hosted_zone_id=hosted_zone_id, record_name=record_name)

        jsii.create(CdkApexCname, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        """
        return
        :return: the ARN of the Lambda Function
        """
        return jsii.get(self, "functionArn")


@jsii.data_type(jsii_type="cdk-apex-cname.CdkApexCnameProps", jsii_struct_bases=[], name_mapping={'apex_cname_rule_cron': 'apexCnameRuleCron', 'apex_name': 'apexName', 'hosted_zone_id': 'hostedZoneId', 'record_name': 'recordName'})
class CdkApexCnameProps():
    def __init__(self, *, apex_cname_rule_cron: str, apex_name: str, hosted_zone_id: str, record_name: str):
        """
        :param apex_cname_rule_cron: -
        :param apex_name: The properties for the Apex Cname Lambda.
        :param hosted_zone_id: -
        :param record_name: -
        """
        self._values = {
            'apex_cname_rule_cron': apex_cname_rule_cron,
            'apex_name': apex_name,
            'hosted_zone_id': hosted_zone_id,
            'record_name': record_name,
        }

    @builtins.property
    def apex_cname_rule_cron(self) -> str:
        return self._values.get('apex_cname_rule_cron')

    @builtins.property
    def apex_name(self) -> str:
        """The properties for the Apex Cname Lambda."""
        return self._values.get('apex_name')

    @builtins.property
    def hosted_zone_id(self) -> str:
        return self._values.get('hosted_zone_id')

    @builtins.property
    def record_name(self) -> str:
        return self._values.get('record_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CdkApexCnameProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["CdkApexCname", "CdkApexCnameProps", "__jsii_assembly__"]

publication.publish()
