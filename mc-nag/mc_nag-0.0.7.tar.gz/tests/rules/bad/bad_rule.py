"""Bad rule for testing."""

from mc_nag.base_utils.models.rule import BaseRule


class BadRule(BaseRule):  # pylint: disable=abstract-method
    """Create a bad rule for testing."""

    # rule_id missing
    description = """Testing bad rules."""
    # severity missing
    url = 'https://github.com/stelligent/mc-nag/blob/master/tests/rules/' + \
          'bad/bad_rule.py'
    resolution = 'N/A'
    category_tags = {"custom-resource"}
    source_tags = {"stelligent"}

    # evaluate() missing
