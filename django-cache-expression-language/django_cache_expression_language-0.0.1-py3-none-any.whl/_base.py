from abc import ABC
from inspect import Signature
from re import findall, split
from typing import Dict

from django.core.cache import caches


class BaseCacheDecorator(ABC):

    def __init__(self, key: str, alias: str):
        self.key_expr = key
        self.alias = alias
        self.cache = caches[alias]

    def _get_key(self, signature: Signature, *args, **kwargs) -> str:
        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        value_per_expr = self._get_value_per_variable_expression(
            self.key_expr, bound_arguments.arguments
        )

        key = self.key_expr
        for expr, value in value_per_expr.items():
            key = key.replace(expr, value)

        return key

    @staticmethod
    def _get_value_per_variable_expression(
            expression: str, arguments: Dict[str, object]
    ) -> Dict[str, str]:
        value_per_expr = {}

        for variable_expr in findall(r'(?<={).*?(?=\})', expression):
            attributes = split(r'\W+', variable_expr)
            argument_key = attributes[0]
            argument_attributes = attributes[1:]

            argument_value = arguments[argument_key]
            for attribute in argument_attributes:
                argument_value = (
                    argument_value.__getitem__(attribute)
                    if isinstance(argument_value, dict)
                    else argument_value.__getitem__(int(attribute))
                    if isinstance(argument_value, list)
                       or isinstance(argument_value, tuple)
                    else argument_value.__getattribute__(attribute)
                )
            argument_value = str(argument_value)

            value_per_expr[f'{{{variable_expr}}}'] = argument_value

        return value_per_expr
