from abc import ABC
from inspect import Signature
from re import finditer
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
        key = self._get_parsed_expression(self.key_expr, bound_arguments.arguments)
        return key

    @staticmethod
    def _get_parsed_expression(expression: str, arguments: Dict[str, object]) -> str:
        parsed_exprs = []
        for variable_expr_match in finditer(r'[^{}]+|{[^{}]+}', expression):
            variable_expr = variable_expr_match.group()
            if variable_expr.startswith('{'):
                argument_value = arguments
                for attribute_expr_match in finditer(r'\.?[a-zA-Z0-9_]+|\[[^\[\]]+\]', variable_expr):
                    attribute_expr = attribute_expr_match.group()
                    if attribute_expr.startswith('["') or attribute_expr.startswith('[\''):
                        index = attribute_expr[2:-2]
                        argument_value = argument_value.__getitem__(index)
                    elif attribute_expr.startswith('['):
                        index = int(attribute_expr[1:-1])
                        argument_value = argument_value.__getitem__(index)
                    elif attribute_expr.startswith('.'):
                        index = attribute_expr[1:]
                        argument_value = argument_value.__getattribute__(index)
                    else:
                        index = attribute_expr
                        argument_value = argument_value.__getitem__(index)
                argument_value = str(argument_value)
            else:
                argument_value = variable_expr
            parsed_exprs.append(argument_value)
        return ''.join(parsed_exprs)
