"""Tests for BaseRule."""

from pytest import raises, warns
from mc_nag.base_utils.exceptions import MissingAttributeError
from mc_nag.base_utils.models.rule import BaseRule

TEMPLATE_MODEL = {'raw': 'model'}
OBJECT_ID = '001'


def test_base_rule_good_subclass():
    """Happy Path: Ensure subclass can create with required attributes."""
    class GoodSubclassBaseRule(BaseRule):
        """Create subclass of BaseRule with required attributes."""

        rule_id = OBJECT_ID
        description = 'This is a rule that properly instantiates BaseRule.'
        severity = 'FAIULRE'
        url = 'http://rule.documentation/'
        resolution = 'Take these actions to fix the violation.'
        category_tags = {"storage"}
        source_tags = {"stelligent"}

        def evaluate(self):
            """Logic to implement the rule."""
            return self.template_model

    good_object = GoodSubclassBaseRule(TEMPLATE_MODEL)

    assert good_object.rule_id == OBJECT_ID
    assert good_object.evaluate() == TEMPLATE_MODEL


def test_base_rule_bad_subclass():
    """Sad Path: Catch error when subclass is missing attributes."""
    # pylint: disable=too-few-public-methods,abstract-method
    class RuleMissingAttributes(BaseRule):
        """Create subclass of BaseRule without setting all attributes."""

        description = 'This is a rule that properly instantiates BaseRule.'
        severity = 'FAIULRE'
        url = 'http://rule.documentation/'
        category_tags = {"storage"}
        source_tags = {"stelligent"}

    with raises(MissingAttributeError,
                match=r"must define.*attribute\(s\)!"):
        _ = RuleMissingAttributes(TEMPLATE_MODEL)

    class RuleMissingEvaluate(BaseRule):
        """Create subclass of BaseRule without evaluate() method."""

        rule_id = OBJECT_ID
        description = 'This is a rule that properly instantiates BaseRule.'
        severity = 'FAIULRE'
        url = 'http://rule.documentation/'
        resolution = 'This is how you fix this violation.'
        category_tags = {"storage"}
        source_tags = {"stelligent"}

    rule_missing_evaluate = RuleMissingEvaluate(TEMPLATE_MODEL)
    with raises(MissingAttributeError,
                match=r"must implement an evaluate\(\) method with logic"):
        rule_missing_evaluate.evaluate()


def test_tags_issue_warning():
    """Sad Path: Show the user a warning if a Rule doesn't have a tag."""
    class TagsMissing(BaseRule):
        """Show warning on subclasses of BaseRule without tags."""

        rule_id = OBJECT_ID
        description = 'This is a rule has no tags.'
        severity = 'FAIULRE'
        url = 'http://rule.documentation/'
        resolution = 'This is how you fix this violation.'

        def evaluate(self):
            pass

    with warns(UserWarning, match=r"tags properties are optional."):
        TagsMissing(TEMPLATE_MODEL)


def test_tag_cleaning():
    """Happy Path: Make sure tags are lowercased and text only."""
    class TagCleaned(BaseRule):
        """Ensure that tags are cleaned and valid."""

        rule_id = OBJECT_ID
        description = 'This is a rule that properly instantiates BaseRule.'
        severity = 'FAIULRE'
        url = 'http://rule.documentation/'
        resolution = 'This Class is valid.'
        category_tags = {"STORAGE"}
        source_tags = {"SteLLigent"}

        def evaluate(self):
            pass

    clean_rule = TagCleaned(TEMPLATE_MODEL)
    assert clean_rule.clean_category_tags == {"storage"}
    assert clean_rule.clean_source_tags == {"stelligent"}

    class TagsWithNumber(BaseRule):
        """Ensure that tags are cleaned and valid."""

        rule_id = OBJECT_ID
        description = 'This is a rule that properly instantiates BaseRule.'
        severity = 'FAIULRE'
        url = 'http://rule.documentation/'
        resolution = 'This Class is valid.'
        category_tags = {"StorAGE", 2600}
        source_tags = {"SteLLigent", 7200}

        def evaluate(self):
            pass

    remove_numbers = TagsWithNumber(TEMPLATE_MODEL)
    assert remove_numbers.clean_category_tags == {"storage"}
    assert remove_numbers.clean_source_tags == {"stelligent"}
