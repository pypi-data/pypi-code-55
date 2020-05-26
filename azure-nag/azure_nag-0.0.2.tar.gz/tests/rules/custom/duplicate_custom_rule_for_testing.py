"""Rule to test the duplicate rules check."""

from mc_nag.base_utils.models.rule import (
    BaseRule,
    WARNING as RULE_WARNING
)


class DuplicateCustomPlatformRule(BaseRule):
    """Create a duplicate custom rule to test duplicate rules check."""

    rule_id = 'custom-platform-rule-test'
    description = """Testing the duplicate rules check."""
    severity = RULE_WARNING
    url = 'https://github.com/stelligent/mc-nag/tests/rules/custom/' + \
          'duplicate_custom_rule_for_testing.py'
    category_tags = {'custom-resource'}
    source_tags = {'stelligent'}
    resolution = 'N/A'
    category_tags = {"custom-resource"}
    source_tags = {"stelligent"}

    def evaluate(self):
        """Return all resources."""
        return self.template_model.resources
