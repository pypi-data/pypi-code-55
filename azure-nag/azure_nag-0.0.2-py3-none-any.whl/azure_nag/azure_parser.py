"""AzureParser class."""

from mc_nag.base_utils.parser import BaseParser
from azure_nag.azure_parser_interpolator import AzureParserInterpolator


class AzureParser(BaseParser):
    """Parser class to interpret raw Azure Resource Manager templates."""

    # Dictionary of RegEx patterns that can be picked up in an ARM template
    # resource's property and interpolated
    REGEX_DICT = {
        # Example for below: "[parameters('secret_url')]"
        "PARAMETER_REGEX":
            r"^\[parameters\(\'(.*?)\'\)\]$",

        # Example for below: "[variables('osType')]"
        "VARIABLE_REGEX":
            r"^\[variables\(\'(.*?)\'\)\]$",

        # Example for below: "[variables('environmentSettings')[parameters('environmentName')]]"
        "VARIABLE_PARAMETER_REGEX":
            r"^\[variables\(\'(.*?)\'\)\[parameters\(\'(.*?)\'\)\]\]$",

        # Example for below:
        # "[variables('environmentSettings')[parameters('alternateEnvironmentName')].instanceSize]"
        "VARIABLE_PARAMETER_NESTED_KEY_REGEX":
            r"^\[variables\(\'(.*?)\'\)\[parameters\(\'(.*?)\'\)\]\.(.*?)\]$",

        # Example for below: "[variables('disk_iops_read_write').iops]"
        "VARIABLE_NESTED_KEY_REGEX":
            r"^\[variables\(\'(.*?)\'\)\.(.*?)\]$"
    }

    TEMPLATE_REQUIRED_KEYS = ['$schema', 'contentVersion', 'resources']
    PARAMETERS_FILE_REQUIRED_KEYS = ['$schema', 'contentVersion', 'parameters']

    def validate_file(self,
                      file_type=None,
                      parsed_contents=None,
                      required_keys=None,
                      exception_class=Exception):  # pylint: disable=W0613
        """Validate Azure Resource Manager template or Parameters file has required keys.

        :param file_type: One of 'Template' or 'Parameter'.
        :param parsed_contents: Actual contents of file.
        :param required_keys: List of keys required in the file.
        :param exception_class: Type of exception to raise in case of emergency.
        """
        if file_type == 'Template':
            super().validate_file(file_type='Template',
                                  parsed_contents=self.parsed_template,
                                  required_keys=AzureParser.TEMPLATE_REQUIRED_KEYS)
        elif file_type == 'Parameter':
            if parsed_contents is not None:
                super().validate_file(file_type='Parameter',
                                      parsed_contents=self.parsed_parameter_file,
                                      required_keys=AzureParser.PARAMETERS_FILE_REQUIRED_KEYS)
            else:
                pass

    @staticmethod
    def resolve_value(prop, params_list, variables_list, re_dict):
        """Attempt to resolve a property's value.

        Checks to see if the property is a parameter/variable reference and if so, then attempts
        to resolve that property's value by replacing it with constructed value from the
        reference using RegEx logic. If the property is not a not reference, then just
        returns the raw value of that property.

        :param prop: Property name to resolve.
        :param params_list: List of parameters from which to pull values.
        :param variables_list: List of variables from which to pull values.
        :param re_dict: Dictionary of regex patterns to determine logic to execute.
        """
        for key, _ in re_dict.items():
            if AzureParserInterpolator.get_regex_groups(prop, re_dict, key):
                prop_re_groups = AzureParserInterpolator.get_regex_groups(prop, re_dict, key)
                regex_method = getattr(AzureParserInterpolator, f'resolve_{key.lower()}')
                resolved_property = regex_method(prop_re_groups, variables_list, params_list)
                if resolved_property is not None:
                    return resolved_property
        return prop

    @staticmethod
    def resolve_values_in_properties(res_properties, params_list, variables_list, re_dict):
        """Attempt to resolve a resource's set of property values.

        Iterates through a resource's set of properties and attempts to resolve each
        property's value that is a reference to a parameter/variable.

        :param res_properties: One or more properties from the resource to resolve.
        :param params_list: List of parameters from which to pull values.
        :param variables_list: List of variables from which to pull values.
        :param re_dict: Dictionary of regex patterns to determine logic to execute.
        """
        # Return resolved value for a string
        if isinstance(res_properties, str):
            return AzureParser.resolve_value(res_properties, params_list,
                                             variables_list, re_dict)

        # Iterate over items in list and resolve each value
        if isinstance(res_properties, list):
            return [
                AzureParser.resolve_values_in_properties(
                    item,
                    params_list,
                    variables_list,
                    re_dict)
                for item in res_properties
            ]

        # Iterate over items in dict and resolve each nested value
        if isinstance(res_properties, dict):
            resolved_properties = {}

            for key, value in res_properties.items():
                resolved_properties[key] = AzureParser.resolve_values_in_properties(
                    value, params_list, variables_list, re_dict)

            return resolved_properties

        # Return original value if type not handled
        return res_properties
