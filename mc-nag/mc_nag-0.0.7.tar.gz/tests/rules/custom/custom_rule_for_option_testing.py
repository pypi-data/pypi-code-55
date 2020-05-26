"""Rule to test the --custom-platform-rules-dir Click option."""

from mc_nag.base_utils.models.rule import (
    BaseRule,
    WARNING as RULE_WARNING
)


class CustomPlatformRule(BaseRule):
    """Create a custom rule to test --custom-platform-rules-dir option."""

    rule_id = 'custom-platform-rule-test'
    description = """Testing the --custom-platform-rules-dir option."""
    severity = RULE_WARNING
    url = 'https://github.com/stelligent/mc-nag/tests/rules/custom/' + \
          'custom_rule_for_option_testing.py'
    resolution = 'N/A'
    category_tags = {"custom-resource"}
    source_tags = {"stelligent"}

    def evaluate(self):
        """Find storageAccount resources and validate 'encryption' property.

        1. Obtain a list of storageAccount resources.
        2. Search their properties for 'encryption'.
        3. Ensure at least one service is enabled.
        4. Ensure keySource subproperty is set.
        """
        return self.template_model.resources
