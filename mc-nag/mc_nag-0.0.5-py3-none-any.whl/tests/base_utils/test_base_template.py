"""Tests for BaseTemplate."""

from pytest import raises
from mc_nag.base_utils.models.template import BaseTemplate

TEMPLATE_PATH = 'tests/templates/base'


def test_base_template_good_subclass():
    """Happy Path: Ensure subclass can create with required attributes."""
    class GoodSubclassBaseTemplate(BaseTemplate):
        """Create subclass of BaseTemplate with required attributes."""

        def __init__(self, template_string):
            """Init GoodSubclassBaseTemplate."""
            self.template_string = template_string
            self.parsed_template = 'This is a good parsed template'

        @property
        def resources(self):
            """List of template resources."""
            return []

        @property
        def parameters(self):
            """List of template parameters."""
            return []

        @property
        def functions(self):
            """List of template functions."""
            return []

        @property
        def variables(self):
            """List of template variables."""
            return []

        @property
        def outputs(self):
            """List of template outputs."""
            return []

    good_template_string = 'Good template string'
    good_object = GoodSubclassBaseTemplate(good_template_string)

    assert len(good_object.resources) == 0
    assert good_object.template_string == good_template_string
    assert good_object.parsed_template == 'This is a good parsed template'


def test_base_template_bad_subclass():
    """Sad Path: Catch error when subclass is missing attributes."""
    # pylint: disable=too-few-public-methods
    class BadSubclassBaseTemplate(BaseTemplate):
        """Create subclass of BaseTemplate without setting all attributes."""

        def __init__(self, template_string):
            """Init BadSubclassBaseTemplate."""
            self.wrong_template_string = template_string
            self.wrong_parsed_template = 'This is a bad parsed template'

    bad_template_string = 'Bad subclass'

    with raises(NotImplementedError,
                match=r"must define.*attribute\(s\) as type 'list'"):
        _ = BadSubclassBaseTemplate(bad_template_string)
