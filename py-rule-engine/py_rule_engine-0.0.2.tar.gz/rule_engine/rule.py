from collections import namedtuple
from typing import Dict

from rule_engine.error import RequiredFieldsMissing

Rule = namedtuple("Rule", ["dimension", "operator", "value"])


class RuleSet:

    rules: [Rule]

    def __init__(self, rules: [Rule]):
        self.rules = rules

    def _validate_context(self, context: Dict):
        for rule in self.rules:
            value = context.get(rule.dimension)
            if value is None:
                raise RequiredFieldsMissing(
                    f"Missing required field : {rule.dimension}"
                )
        return True

    def _evaluate_rule(self, rule, context):
        resolved_value = context.get(rule.dimension)
        if rule.operator.is_binary:
            return rule.operator.apply(resolved_value, rule.value)
        return rule.operator.apply(resolved_value)

    def evaluate(self, context: Dict) -> bool:
        self._validate_context(context)
        result = True
        for rule in self.rules:
            result = result and self._evaluate_rule(rule, context)
        return result
