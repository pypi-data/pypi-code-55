"""Describe a generic template in Python memory."""

from mc_nag.base_utils.metaclasses import RequiredAttributeDefinitionMeta


# pylint: disable=too-few-public-methods
class BaseTemplate(metaclass=RequiredAttributeDefinitionMeta):
    """Define an extensible base template class with required attributes.

    One can subclass this BaseTemplate class as a normal python subclass, but
    also must ensure the required attributes are included.

    Example:
    | from base_utils.models.template import BaseTemplate
    |
    | def NewTemplate(BaseTemplate):
    |     '''This is a new template.'''
    |
    |     def __init__(self, new_template_string):
    |         '''Initialze NewTemplate object.'''
    |         self.template_string = new_template_string
    |         self.parsed_template = NewParser(new_template_string)
    |
    |     @property
    |     def resources(self):
    |         '''Return list of resources in the template.'''
    |         return [resource for resources in ...]
    |
    |     ...

    :attr template_string: Raw string read from the template file.
    :attr parsed_template: Output from the platform's parser object.
    :attr resources: List of platform-specific resources in the template.
    :attr parameters: List of platform-specific parameters in the template.
    :attr outputs: List of platform-specific outputs in the template.
    :attr functions: List of platform-specific functions in the template.
    :attr variables: List of platform-specific variables in the template.
    """

    template_string = None
    parsed_template = None
    resources = None
    parameters = None
    outputs = None
    functions = None
    variables = None
    required_attributes = [
        'template_string',
        'parsed_template',
        'resources',
        'parameters',
        'outputs',
        'functions',
        'variables'
    ]

    def find_resources_by_type(self, resource_type: str):
        """Return list of resources matching the given type."""
        return [res for res in self.resources
                if res.resource_type == resource_type]

    def check_required_attributes(self):
        """Ensure required properties are set."""
        missing_attributes = [
            attr for attr in self.required_attributes
            if attr not in ['template_string', 'parsed_template'] and  # noqa: W504
            not isinstance(getattr(self, attr), list)
        ]
        if not self.template_string:
            missing_attributes.append('template_string')
        if not self.parsed_template:
            missing_attributes.append('parsed_template')

        if missing_attributes:
            raise NotImplementedError(
                f'Class \'{self.__class__.__name__}\' must define ' +  # noqa: W504
                f'{missing_attributes} attribute(s) as type \'list\''
            )

    def __repr__(self):
        """Print debugging output for template models.

        :param template_model: Data model of a platform's template.
        """
        item_divider_char = '+'
        item_divider_length = 15
        item_divider = ''.rjust(item_divider_length, item_divider_char)

        # Resources
        repr_string = _repr_section_divider('RESOURCES')
        for res in self.resources:
            repr_string += f"""Resource Name: {res.resource_name}
Resource Type: {res.resource_type}
Resource Properties: {res.properties}
Resource Line Number: {res.line_number}
{item_divider}\n"""

        # Parameters
        repr_string += _repr_section_divider('PARAMETERS')
        for param in self.parameters:
            repr_string += f"""Parameter Name: {param.parameter_name}
Parameter Value: {param.parameter_value}
Parameter Type: {param.parameter_type}
{item_divider}\n"""

        # Outputs
        repr_string += _repr_section_divider('OUTPUTS')
        for output in self.outputs:
            repr_string += f"""Output Name: {output.output_name}
Output Value: {output.output_value}
Output Type: {output.output_type}
{item_divider}\n"""

        # Functions
        repr_string += _repr_section_divider('FUNCTIONS')
        for function in self.functions:
            repr_string += f"""Function Namespace: {function.function_namespace}
Function Members: {function.function_members}
{item_divider}\n"""

        # Variables
        repr_string += _repr_section_divider('VARIABLES')
        for variable in self.variables:
            repr_string += f"""Variable Name: {variable.variable_name}
Variable Value: {variable.variable_value}
{item_divider}\n"""
        repr_string += _repr_section_divider()

        return repr_string


def _repr_section_divider(title=None):
    """Return formatted string for __repr__ section dividers."""
    divider_char = '='
    divider_length = 53
    divider = ''.rjust(divider_length, divider_char)

    if title:
        return f"{divider}\n{title}\n{divider}\n"

    return divider
