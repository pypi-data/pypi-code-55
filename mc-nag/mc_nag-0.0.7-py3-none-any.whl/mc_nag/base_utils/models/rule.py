"""Describe a generic rule class."""

import warnings

from mc_nag.base_utils.exceptions import MissingAttributeError
from mc_nag.base_utils.metaclasses import RequiredAttributeDefinitionMeta

ERROR = 'ERROR'
WARNING = 'WARNING'
STYLE = 'STYLE'


class BaseRule(metaclass=RequiredAttributeDefinitionMeta):
    """Define an extensible base rule class with required attributes.

    One can subclass this BaseRule class as a normal python subclass, but also
    must ensure the required attributes are included and the evaluate()
    function is overridden.

    Example:
    | from base_utils.models.rule import (
    |     BaseRule,
    |     WARNING as RULE_WARNING
    | )
    |
    | def NewRule(BaseRule):
    |     '''This is a new rule.'''
    |
    |     rule_id = '001'
    |     description = 'This is a new rule.'
    |     severity = RULE_WARNING
    |     url = 'https://rule.info/'
    |     resolution = 'Instructions how to fix the violations.'
    |
    |     def evaluate(self):
    |         '''Logic to implement the rule.'''
    |         pass

    To instantiate the rule, the template model must be the only argument.

    Example:
    | rule_object = NewRule(template_model)


    :param template_model: Data model object from the associated platform's
                           template class.

    :attr rule_id: Unique identifier for the rule.
    :attr description: Short description of what the rule is checking.
    :attr severity: Category of the violation (ERROR, WARNING, or STYLE).
    :attr url: Link to more information about the rule.
    :attr resolution: Instructions on how to fix violations of the rule.
    :attr category_tags: Set by the Rule author.
    :attr source_tags: Set by the Rule author.
    :attr clean_category_tags: Validated category names
          (e.g. "storage", "security", "networking")
    :attr clean_source_tags: Validated source names
          (e.g. "company_name", "team_name", "creator_name")
    """

    __exclude_from_evaluation = True

    rule_id = None
    description = None
    severity = None
    url = None
    resolution = None
    category_tags = None
    source_tags = None
    required_attributes = [
        'rule_id',
        'description',
        'severity',
        'url',
        'resolution'
    ]

    def __init__(self, template_model, rule_params=None):
        """Assign template_model as an attribute."""
        self.template_model = template_model
        self.__set_tags()
        if rule_params:
            for param in rule_params:
                setattr(self, param.split('=')[0], param.split('=')[1])

    def check_required_attributes(self):
        """Ensure required properties are set."""
        missing_attributes = [attr for attr in self.required_attributes
                              if getattr(self, attr) is None]
        if missing_attributes:
            raise MissingAttributeError(
                f'Class \'{self.__class__.__name__}\' must define ' +  # noqa: W504
                f'{missing_attributes} attribute(s)!'
            )

    def evaluate(self):
        """Implement rule logic.

        Any logic needed to detect violating resources should be implemented
        in this function.

        :return: List of violating resource objects.
        """
        raise MissingAttributeError(
            f'Class \'{self.__class__.__name__}\' must implement an ' +  # noqa: W504
            'evaluate() method with logic to implement rule!'
        )

    def __clean_tags(self, dirty_tags):  # pylint: disable=no-self-use
        """Sanitize tags for consistency.

        :return: A set data type of lowercase strings.
        """
        result = set(x.lower() for x in dirty_tags if isinstance(x, str))
        return result

    def __process_tags(self, evaluate_tags):
        """Type checks tags.

        Issues a warning if no tags are set.

        :return: Set of lowercase string tags or an empty set.
        """
        if isinstance(evaluate_tags, set):
            result = self.__clean_tags(evaluate_tags)
        else:
            warnings.warn(
                f"""Class \'{self.__class__.__name__}\' tags properties are optional.
                    When configured, use a Set of lowercase
                    strings. e.g. {{"storage"}}""", UserWarning, stacklevel=2)
            result = set()
        return result

    def __set_tags(self):
        """Assign sanitized tags."""
        self.clean_category_tags = self.__process_tags(self.category_tags)
        self.clean_source_tags = self.__process_tags(self.source_tags)
