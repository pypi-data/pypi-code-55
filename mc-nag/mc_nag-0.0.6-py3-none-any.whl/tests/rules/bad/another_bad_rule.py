"""Another bad rule for testing."""

from mc_nag.base_utils.models.rule import BaseRule


class AnotherBadRule(BaseRule):  # pylint: disable=abstract-method
    """Create another bad rule for testing."""

    # rule_id missing
    description = """Testing bad rules."""
    # severity missing
    url = 'https://github.com/stelligent/mc-nag/blob/master/tests/rules/' + \
          'bad/another_bad_rule.py'
    resolution = 'N/A'
    category_tags = {"custom-resource"}
    source_tags = {"stelligent"}

    # evaluate() missing
