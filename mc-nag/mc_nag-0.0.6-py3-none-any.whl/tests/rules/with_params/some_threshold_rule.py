"""Rule to test passing params into rules."""

from mc_nag.base_utils.models.rule import (
    BaseRule,
    WARNING as RULE_WARNING
)


class RuleWithSomeThresholdParameter(BaseRule):
    """Create a custom rule to test passing params."""

    rule_id = 'some-threshold-rule'
    description = """Testing the passing of params into rules."""
    severity = RULE_WARNING
    url = 'https://github.com/stelligent/mc-nag/tests/rules/with_params/' + \
          'some_threshold_rule.py'
    resolution = 'N/A'
    category_tags = {"custom-resource"}
    source_tags = {"stelligent"}

    some_threshold = 0


    def evaluate(self):
        """Find storageAccount resources and validate 'encryption' property.

        1. Obtain a list of storageAccount resources.
        2. Search their properties for 'encryption'.
        3. Ensure at least one service is enabled.
        4. Ensure keySource subproperty is set.
        """
        print(f'self.some_threshold == {self.some_threshold}')
        return self.template_model.resources
