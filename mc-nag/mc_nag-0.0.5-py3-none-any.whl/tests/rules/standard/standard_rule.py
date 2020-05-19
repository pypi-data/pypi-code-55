"""Standard rule for testing."""

from mc_nag.base_utils.models.rule import (
    BaseRule,
    WARNING as RULE_WARNING
)


class StandardRule(BaseRule):
    """Create a standard rule for testing."""

    rule_id = 'standard-rule'
    description = """Testing standard rules."""
    severity = RULE_WARNING
    url = 'https://github.com/stelligent/mc-nag/tests/rules/standard/' + \
          'standard_rule.py'
    resolution = 'N/A'
    category_tags = {"custom-resource"}
    source_tags = {"stelligent"}

    def evaluate(self):
        """Return empty list."""
        return []
