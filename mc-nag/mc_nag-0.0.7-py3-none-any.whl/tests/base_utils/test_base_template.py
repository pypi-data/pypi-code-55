"""Tests for BaseTemplate."""

from pytest import raises
from mc_nag.base_utils.models.template import BaseTemplate


class BasicResource():
    """Basic resource."""

    def __init__(self, rname, rtype, rproperties, rraw, rline):
        """Create a basic resource object."""
        self.resource_name = rname
        self.resource_type = rtype
        self.properties = rproperties
        self.raw_string = rraw
        self.line_number = rline


class GoodSubclassBaseTemplate(BaseTemplate):
    """Create subclass of BaseTemplate with required attributes."""

    def __init__(self, template_string, resource_list=None):
        """Init GoodSubclassBaseTemplate."""
        self.template_string = template_string
        self.parsed_template = 'This is a good parsed template'
        self._resources = resource_list if resource_list else []

    @property
    def resources(self):
        """List of template resources."""
        return self._resources

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


# pylint: disable=too-few-public-methods
class BadSubclassBaseTemplate(BaseTemplate):
    """Create subclass of BaseTemplate without setting all attributes."""

    def __init__(self, template_string):
        """Init BadSubclassBaseTemplate."""
        self.wrong_template_string = template_string
        self.wrong_parsed_template = 'This is a bad parsed template'


def test_base_template_good_subclass():
    """Happy Path: Ensure subclass can create with required attributes."""
    good_template_string = 'Good template string'
    good_object = GoodSubclassBaseTemplate(good_template_string)

    assert len(good_object.resources) == 0
    assert good_object.template_string == good_template_string
    assert good_object.parsed_template == 'This is a good parsed template'


def test_base_template_bad_subclass():
    """Sad Path: Catch error when subclass is missing attributes."""
    bad_template_string = 'Bad subclass'

    with raises(NotImplementedError,
                match=r"must define.*attribute\(s\) as type 'list'"):
        _ = BadSubclassBaseTemplate(bad_template_string)


def test_base_template_resources_by_type():
    """Happy Path: Ensure we can find resources by type."""
    good_template_string = 'Good template string'
    good_object = GoodSubclassBaseTemplate(
        good_template_string,
        [
            BasicResource('res1', 'typeA', {'prop1': 'val1'}, 'res1string', 1),
            BasicResource('res2', 'typeA', {'prop2': 'val2'}, 'res2string', 2),
            BasicResource('res3', 'typeB', {'prop3': 'val3'}, 'res3string', 3)
        ]
    )

    assert len(good_object.resources) == 3
    assert good_object.template_string == good_template_string
    assert good_object.parsed_template == 'This is a good parsed template'
    type_a_resources = good_object.find_resources_by_type('typeA')
    assert len(type_a_resources) == 2
    assert 'res2' in {res.resource_name for res in type_a_resources}
