"""
# jsii-code-samples

> An example jsii package authored in TypeScript that gets published as GitHub packages for Node.js, Python, Java and dotnet.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *


class HelloWorld(metaclass=jsii.JSIIMeta, jsii_type="jsii-code-samples.HelloWorld"):
    def __init__(self) -> None:
        jsii.create(HelloWorld, self, [])

    @jsii.member(jsii_name="fibonacci")
    def fibonacci(self, num: jsii.Number) -> jsii.Number:
        """
        :param num: -
        """
        return jsii.invoke(self, "fibonacci", [num])

    @jsii.member(jsii_name="sayHello")
    def say_hello(self, name: str) -> str:
        """
        :param name: -
        """
        return jsii.invoke(self, "sayHello", [name])


__all__ = [
    "HelloWorld",
]

publication.publish()
