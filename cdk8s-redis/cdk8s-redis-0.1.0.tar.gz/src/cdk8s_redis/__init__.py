"""
# cdk8s-redis

> Redis constructs for cdk8s

Basic implementation of a Redis construct for cdk8s. Contributions are welcome!

## Usage

The following will define a Redis cluster with a master and 2 slave replicas:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk8s_redis import Redis

# inside your chart:
redis = Redis(self, "my-redis")
```

DNS names can be obtained from `redis.masterHost` and `redis.slaveHost`.

You can specify how many slave replicas to define:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Redis(self, "my-redis",
    slave_replicas=4
)
```

Or, you can specify no slave:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Redis(self, "my-redis",
    slave_replicas=0
)
```

## License

Distributed under the [Apache 2.0](./LICENSE) license.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import cdk8s
import constructs

from ._jsii import *


class Redis(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk8s-redis.Redis"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: constructs.Construct, id: str, *, labels: typing.Optional[typing.Mapping[str, str]]=None, slave_replicas: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param labels: Extra labels to associate with resources. Default: - none
        :param slave_replicas: Number of slave replicas. Default: 2

        stability
        :stability: experimental
        """
        options = RedisOptions(labels=labels, slave_replicas=slave_replicas)

        jsii.create(Redis, self, [scope, id, options])

    @builtins.property
    @jsii.member(jsii_name="masterHost")
    def master_host(self) -> str:
        """The DNS host for the master server.

        stability
        :stability: experimental
        """
        return jsii.get(self, "masterHost")

    @builtins.property
    @jsii.member(jsii_name="slaveHost")
    def slave_host(self) -> str:
        """The DNS host for the slave service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "slaveHost")


@jsii.data_type(jsii_type="cdk8s-redis.RedisOptions", jsii_struct_bases=[], name_mapping={'labels': 'labels', 'slave_replicas': 'slaveReplicas'})
class RedisOptions():
    def __init__(self, *, labels: typing.Optional[typing.Mapping[str, str]]=None, slave_replicas: typing.Optional[jsii.Number]=None) -> None:
        """
        :param labels: Extra labels to associate with resources. Default: - none
        :param slave_replicas: Number of slave replicas. Default: 2

        stability
        :stability: experimental
        """
        self._values = {
        }
        if labels is not None: self._values["labels"] = labels
        if slave_replicas is not None: self._values["slave_replicas"] = slave_replicas

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Extra labels to associate with resources.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def slave_replicas(self) -> typing.Optional[jsii.Number]:
        """Number of slave replicas.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('slave_replicas')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RedisOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "Redis",
    "RedisOptions",
]

publication.publish()
