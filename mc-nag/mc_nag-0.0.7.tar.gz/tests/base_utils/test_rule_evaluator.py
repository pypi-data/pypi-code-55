"""Tests for rule evaluation logic."""

import re
from pytest import fixture, raises
from mc_nag.base_utils.exceptions import (
    InvalidParameter,
    MissingAttributeError
)
from mc_nag.base_utils import read_template_file
from mc_nag.base_utils.models.rule import (
    WARNING as RULE_WARNING
)
from mc_nag.base_utils.models.rule_directory import RuleDirectoryManager
from mc_nag.base_utils.rule_evaluator import RuleEvaluator
from tests.rules.standard.standard_rule import StandardRule
from tests.rules.custom.custom_rule_for_option_testing import \
    CustomPlatformRule
from tests.rules.with_params.some_threshold_rule import \
    RuleWithSomeThresholdParameter
from tests.rules.bad.bad_rule import BadRule
from tests.fixtures import TestTemplate

# pylint: disable=redefined-outer-name

TEMPLATES_PATH = 'tests/templates'
VALID_TEMPLATE = f'{TEMPLATES_PATH}/parser_test_good.json'
INVALID_TEMPLATE = f'{TEMPLATES_PATH}/parser_test_bad.json'


@fixture(scope='module')
def valid_template_model():
    """Return template model for a valid template."""
    return TestTemplate(read_template_file(VALID_TEMPLATE))


@fixture(scope='module')
def invalid_template_model():
    """Return template model for an invalid template."""
    return TestTemplate(read_template_file(INVALID_TEMPLATE))


@fixture(scope='module')
def rule_dir_manager():
    """Return standard rules only."""
    return RuleDirectoryManager(True, 'tests/rules/standard', None)


@fixture(scope='module')
def rule_dir_manager_std_and_custom(custom='tests/rules/custom'):
    """Return both standard and custom rules."""
    return RuleDirectoryManager(True, 'tests/rules/standard', custom)


@fixture(scope='module')
def rule_dir_manager_bad():
    """Return bad rules only."""
    return RuleDirectoryManager(True, 'tests/rules/bad', None)


@fixture(scope='module')
def custom_only_rule_dir_manager():
    """Return only custom rules."""
    return RuleDirectoryManager(False, '', 'tests/rules/custom')


def test_rule_evaluator_standard_rules(rule_dir_manager):
    """Happy Path: Ensure we can import standard rules."""
    rule_evaluator = RuleEvaluator(None, rule_dir_manager)

    assert StandardRule.__name__ in \
        [rule.__name__ for rule in rule_evaluator.rule_set]


def test_rule_evaluator_custom_rules(rule_dir_manager_std_and_custom):
    """Happy Path: Ensure we can import custom rules."""
    rule_evaluator = RuleEvaluator(None, rule_dir_manager_std_and_custom)

    rule_names = [rule.__name__ for rule in rule_evaluator.rule_set]
    assert StandardRule.__name__ in rule_names
    assert CustomPlatformRule.__name__ in rule_names


def test_rule_evaluator_only_custom_rules(custom_only_rule_dir_manager):
    """Happy Path: Ensure we can import only custom rules."""
    rule_evaluator = RuleEvaluator(None, custom_only_rule_dir_manager)

    rule_names = [rule.__name__ for rule in rule_evaluator.rule_set]
    assert StandardRule.__name__ not in rule_names
    assert CustomPlatformRule.__name__ in rule_names


def test_rule_evaluator_no_rules():
    """Sad Path: Ensure we can handle the case when no rules are supplied.

    This should never happen, as it is handled by Click in main.py,
    but good to validate we will get an empty rule_set.
    """
    with raises(InvalidParameter, match="RuleEvaluator requires the `rule_dir_manager`"):
        RuleEvaluator(None, None)


def test_rule_evaluator_passing_template(valid_template_model, rule_dir_manager):
    """Happy Path: Ensure we can evaluate a rule against a valid template."""
    rule_evaluator = RuleEvaluator(valid_template_model,
                                   rule_dir_manager)
    rule_evaluator.rule_set = set([StandardRule])
    violations_by_rule, violation_counts, rules = rule_evaluator.evaluate_rules()

    assert not violations_by_rule
    assert not violation_counts
    assert rules == {StandardRule}


def test_rule_evaluator_failing_rule(invalid_template_model, rule_dir_manager_std_and_custom):
    """Sad Path: Ensure we can evaluate a rule which returns violations."""
    rule_evaluator = RuleEvaluator(invalid_template_model,
                                   rule_dir_manager_std_and_custom)
    rule_evaluator.rule_set = set([CustomPlatformRule])
    violations_by_rule, violation_counts, rules = rule_evaluator.evaluate_rules()

    assert CustomPlatformRule in violations_by_rule
    assert len(violations_by_rule[CustomPlatformRule]) == 1
    assert RULE_WARNING in violation_counts
    assert violation_counts[RULE_WARNING] == 1
    assert rules == {CustomPlatformRule}


def test_rule_evaluator_bad_rule(invalid_template_model, rule_dir_manager):
    """Sad Path: Ensure we raise an exception for a bad rule class."""
    rule_evaluator = RuleEvaluator(invalid_template_model,
                                   rule_dir_manager)
    rule_evaluator.rule_set = set([BadRule])

    with raises(MissingAttributeError, match="'BadRule' must define"):
        _, _, _ = rule_evaluator.evaluate_rules()


def test_rule_evaluator_display_rules_no_dupes(capsys, rule_dir_manager):
    """Happy Path: Display rules without duplicates."""
    RuleEvaluator(None, rule_dir_manager).display_rules()

    captured_no_dupes = capsys.readouterr()
    assert re.search('No duplicates', captured_no_dupes.out)
    assert re.search(r'standard-rule.*StandardRule', captured_no_dupes.out)


def test_rule_evaluator_display_rules_with_dupes(capsys, rule_dir_manager_std_and_custom):
    """Happy Path: Display rules with duplicates."""
    RuleEvaluator(None, rule_dir_manager_std_and_custom).display_rules()

    captured = capsys.readouterr()
    assert re.search('Found duplicate rule IDs!', captured.out)
    assert re.search(r'Duplicate Rule ID.*Duplicate Rule Names', captured.out)
    assert re.search(
        r'DuplicateCustomPlatformRule \(duplicate_custom_rule_for_testing.py',
        captured.out
    )


def test_rule_evaluator_display_rules_bad(rule_dir_manager_bad):
    """Sad Path: Display rules with duplicates."""
    with raises(MissingAttributeError, match=r"Class .* must define .* attribute\(s\)!"):
        RuleEvaluator(None, rule_dir_manager_bad).display_rules()


def test_rule_evaluator_display_rules_no_rules(capsys, rule_dir_manager):
    """Sad Path: Display evaluator without rules."""
    rule_evaluator = RuleEvaluator(None, rule_dir_manager)
    rule_evaluator.rule_set = set()
    rule_evaluator.display_rules()

    captured = capsys.readouterr()
    assert captured.out == ''


def test_rule_evaluator_rule_params(capsys, valid_template_model):
    """Happy Path: Ensure we can evaluate a rule with parameters passed."""
    some_threshold = 10
    rule_dir = RuleDirectoryManager(False, '', 'tests/rules/with_params')
    rule_evaluator = RuleEvaluator(valid_template_model,
                                   rule_dir,
                                   (f'some_threshold={some_threshold}',
                                    'another_param=unused'))
    assert RuleWithSomeThresholdParameter.__name__ in [
        rule.__name__ for rule in rule_evaluator.rule_set
    ]

    rule_evaluator.rule_set = set([RuleWithSomeThresholdParameter])
    violations_by_rule, violation_counts, rules = rule_evaluator.evaluate_rules()

    assert RuleWithSomeThresholdParameter in violations_by_rule
    assert len(violations_by_rule[RuleWithSomeThresholdParameter]) == 1
    assert RULE_WARNING in violation_counts
    assert violation_counts[RULE_WARNING] == 1
    assert rules == {RuleWithSomeThresholdParameter}
    captured = capsys.readouterr()
    assert re.search(f'self.some_threshold == {some_threshold}', captured.out)


def test_enable_tags_string(rule_dir_manager):
    """Happy Path: Display rules without duplicates."""
    rule_eval = RuleEvaluator(None, rule_dir_manager, None, "string-tag")

    assert isinstance(rule_eval.requested_tags, set)
    assert rule_eval.requested_tags == {"string-tag"}


def test_enable_tags_list(rule_dir_manager):
    """Happy Path: Display rules without duplicates."""
    tags = ["stelligent", "storage"]
    rule_eval = RuleEvaluator(None, rule_dir_manager, None, tags)

    assert isinstance(rule_eval.requested_tags, set)
    assert rule_eval.requested_tags == {"stelligent", "storage"}


def test_enable_tags_tuple(rule_dir_manager):
    """Happy Path: Display rules without duplicates."""
    tags = ("acme-inc", "network")
    rule_eval = RuleEvaluator(None, rule_dir_manager, None, tags)

    assert isinstance(rule_eval.requested_tags, set)
    assert rule_eval.requested_tags == {"acme-inc", "network"}


def test_filter_tags_no_tags(valid_template_model, rule_dir_manager):
    """Happy Path: Display rules without duplicates."""
    rule_eval = RuleEvaluator(valid_template_model, rule_dir_manager, None, None)

    assert rule_eval.requested_tags == set()
