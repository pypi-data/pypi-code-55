"""AzureParser RegEx interpolation helper class."""
import re
from mc_nag.base_utils.exceptions import VariableKeyError


class AzureParserInterpolator:
    """AzureParser Interpolator to resolve ARM template dynamic values."""

    @staticmethod
    def check_variables_list(re_var, vars_list):
        """Checks that requested variable exists within the templates Variables."""
        var_names_list = [var.variable_name for var in vars_list]
        if re_var not in var_names_list:
            raise VariableKeyError(f"Variable '{re_var}' does not exist in Variables list!")

    @staticmethod
    def get_regex_groups(prop, re_dict, re_pattern):
        """Evaluates to true/false if the property's value matches the specified RegEx pattern.

        Also retrieves the RegEx groups that were found from the specified pattern.
        """
        return re.search(re_dict[re_pattern], prop)

    @staticmethod
    def resolve_parameter_regex(prop_re_groups, _=None, params_list=None):
        r"""Attempts to resolve the value for a resource property that references a parameter.

        Uses a RegEx pattern to discover the parameter reference and then resolves the value.

        Example resource property value: "[parameters('secret_url')]"
        Example RegEx pattern: r"^\[parameters\(\'(.*?)\'\)\]$"
        """
        for param in params_list:
            if param.parameter_name == prop_re_groups.group(1):
                if param.parameter_value is not None:
                    return param.parameter_value
        return None

    @staticmethod
    def resolve_variable_regex(prop_re_groups, vars_list=None, _=None):
        r"""Attempts to resolve the value for a resource property that references a variable.

        Uses a RegEx pattern to discover the variable reference and then resolves the value.

        Example resource property value: "[variables('osType')]"
        Example RegEx pattern: r"^\[variables\(\'(.*?)\'\)\]$"
        """
        re_var_name = prop_re_groups.group(1)
        AzureParserInterpolator.check_variables_list(re_var_name, vars_list)
        for var in vars_list:
            if var.variable_name == re_var_name:
                if var.variable_value:
                    return var.variable_value
        return None

    @staticmethod
    def resolve_variable_parameter_regex(prop_re_groups, vars_list=None, params_list=None):
        r"""Attempts to resolve the value for a resource property.

        Attempts to resolve the value for a resource property that references a variable which
        accesses a nested key being the value of a parameter.
        Uses a RegEx pattern to discover this specific pattern then resolves the value.

        Example resource property value:
            "[variables('environmentSettings')[parameters('environmentName')]]"
        Example RegEx pattern:
            r"^\[variables\(\'(.*?)\'\)\[parameters\(\'(.*?)\'\)\]\]$"
        """
        re_var_name = prop_re_groups.group(1)
        AzureParserInterpolator.check_variables_list(re_var_name, vars_list)
        param_value = ''
        for param in params_list:
            if param.parameter_name == prop_re_groups.group(2):
                if param.parameter_value:
                    param_value = param.parameter_value
        for var in vars_list:
            if var.variable_name == re_var_name:
                if var.variable_value:
                    var_dict = var.variable_value
                    try:
                        return var_dict[param_value]
                    except KeyError as err:
                        raise VariableKeyError(
                            f"Variable '{var.variable_name}' does not have a key '{err}'.")
        return None

    @staticmethod
    def resolve_variable_parameter_nested_key_regex(
            prop_re_groups, vars_list=None, params_list=None):
        r"""Attempts to resolve the value for a resource property.

        Attempts to resolve the value for a resource property that references a variable which
        accesses a nested key being the value of a parameter and then a deeper nested key.
        Uses a RegEx pattern to discover this specific pattern then resolves the value.

        Example resource property value:
            "[variables('envSettings')[parameters('envName')].instanceSize]"
        Example RegEx pattern:
            r"^\[variables\(\'(.*?)\'\)\[parameters\(\'(.*?)\'\)\]\.(.*?)\]$"
        """
        re_var_name = prop_re_groups.group(1)
        AzureParserInterpolator.check_variables_list(re_var_name, vars_list)
        param_value = ''
        for param in params_list:
            if param.parameter_name == prop_re_groups.group(2):
                if param.parameter_value:
                    param_value = param.parameter_value
        for var in vars_list:
            if var.variable_name == prop_re_groups.group(1):
                if var.variable_value:
                    var_dict = var.variable_value
                    nested_var_key = prop_re_groups.group(3)
                    try:
                        if var_dict[param_value][nested_var_key]:
                            return var_dict[param_value][nested_var_key]
                    except KeyError as err:
                        raise VariableKeyError(
                            f"Variable '{var.variable_name}' "
                            f"does not have a key or nested key '{err}'.")
        return None

    @staticmethod
    def resolve_variable_nested_key_regex(prop_re_groups, vars_list=None, _=None):
        r"""Attempts to resolve the value for a resource property.

        Attempts to resolve the value for a resource property that references a variable which
        accesses a nested key within that variable's dictionary.
        Uses a RegEx pattern to discover this specific pattern then resolves the value.

        Example resource property value:
            "[variables('disk_iops_read_write').iops]"
        Example RegEx pattern:
            r"^\[variables\(\'(.*?)\'\)\.(.*?)\]$"
        """
        re_var_name = prop_re_groups.group(1)
        AzureParserInterpolator.check_variables_list(re_var_name, vars_list)
        for var in vars_list:
            if var.variable_name == re_var_name:
                if var.variable_value:
                    var_dict = var.variable_value
                    nested_var_key = prop_re_groups.group(2)
                    try:
                        if var_dict[nested_var_key]:
                            return var_dict[nested_var_key]
                    except KeyError as err:
                        raise VariableKeyError(
                            f"Variable '{var.variable_name}' does not have a key '{err}'.")
        return None
