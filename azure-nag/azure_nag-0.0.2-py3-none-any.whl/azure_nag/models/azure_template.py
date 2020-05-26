"""Describe an AzureTemplate in Python memory."""

from mc_nag.base_utils.models.template import BaseTemplate
from mc_nag.base_utils import read_template_file
from ..azure_parser import AzureParser
from .azure_resource import AzureResource
from .azure_parameter import AzureParameter
from .azure_output import AzureOutput
from .azure_function import AzureFunction
from .azure_variable import AzureVariable
from .parameter_helper import check_params_type, \
    check_template_params_default_value, \
    check_file_params_value, \
    check_default_value

# pylint: disable=too-many-instance-attributes

class AzureTemplate(BaseTemplate):
    """Class to model an Azure Resource Manager template."""

    def __init__(self, template_path, parameter_file=None):
        """Initialize AzureObjectModel object."""
        self.template_path = template_path
        self.template_string = read_template_file(template_path)
        # self.parameters_string = None
        # if parameter_file is not None:
        self.parameters_string = read_template_file(parameter_file) \
            if parameter_file is not None else None
        self.parsed_template = AzureParser(self.template_string, self.parameters_string)
        self.parsed_parameter_file = self.parsed_template.parsed_parameter_file
        self._outputs = self._compute_outputs()
        self._functions = self._compute_functions()
        self._variables = self._compute_variables()
        self._parameters = self._compute_parameters()
        self._resources = self._compute_resources()

    @property
    def resources(self):
        """Return computed resources."""
        return self._resources

    @property
    def parameters(self):
        """Return computed parameters."""
        return self._parameters

    @property
    def functions(self):
        """Return computed functions."""
        return self._functions

    @property
    def outputs(self):
        """Return computed outputs."""
        return self._outputs

    @property
    def variables(self):
        """Return computed variables."""
        return self._variables

    def _compute_resources(self):
        """Parse the resources section of Azure Resource Manager templates.

        Create a list of AzureResource to query by other objects during rule
        evaluation.
        Alternate method below for creating dict of resources with key names
        --------------------------------------------------------------------
        def construct_resources_model(self):
            for res in self.parsed_template.resources:
                resource_object = AzureResource(
                    res['type'], res['name'], res['properties'], str(res)
                )
                resource_name = res['name']
                self.resources[resource_name] = {
                    "resource_name": resource_object.resource_name,
                    "resource_type": resource_object.resource_type,
                    "properties": resource_object.properties,
                    "raw_string": resource_object.raw_string
                }
        return: list of AzureResource
        """
        return [
            AzureResource(
                res['type'],
                self.parsed_template.resolve_value(
                    res['name'], self.parameters,
                    self.variables,
                    self.parsed_template.REGEX_DICT),
                self.parsed_template.resolve_values_in_properties(
                    res['properties'],
                    self.parameters,
                    self.variables,
                    self.parsed_template.REGEX_DICT),
                str(res),
                self.parsed_template.find_line_number(
                    f"\"name\": \"{res['name']}\""))
            for res in self.parsed_template.resources]

    def _compute_parameters(self):
        """Create a list of parameters to query by other objects."""
        check_params_type(self.parsed_template.parameters)
        if self.parsed_parameter_file is None:  # pylint: disable=R1705
            check_template_params_default_value(self.parsed_template.parameters)
            return [
                AzureParameter(
                    param_key,
                    param_value['defaultValue'],
                    param_value['type']) for param_key,
                param_value in self.parsed_template.parameters.items()]
        else:
            parameters_list = []
            file_params = self.parsed_parameter_file['parameters']
            check_file_params_value(file_params)
            for param_key, param_value in self.parsed_template.parameters.items():
                if param_key in file_params:
                    resolved_value = file_params[param_key]['value']
                else:
                    check_default_value(param_key, param_value)
                    resolved_value = param_value['defaultValue']

                parameters_list.append(AzureParameter(param_key,
                                                      resolved_value,
                                                      param_value['type']))
            return parameters_list

    def _compute_functions(self):
        """Create a list of functions to query by other objects.

        return: list of AzureFunction
        """
        return [AzureFunction(func['namespace'], func['members'])
                for func in self.parsed_template.functions]

    def _compute_outputs(self):
        """Create a list of outputs to query by other objects.

        return: list of AzureOutput
        """
        return [
            AzureOutput(
                output_key,
                output_value['type'],
                output_value['value']) for output_key,
            output_value in self.parsed_template.outputs.items()]

    def _compute_variables(self):
        """Create a list of variables to query by other objects.

        return: list of AzureVariable
        """
        return [
            AzureVariable(
                variable_key,
                variable_value) for variable_key,
            variable_value in self.parsed_template.variables.items()]
