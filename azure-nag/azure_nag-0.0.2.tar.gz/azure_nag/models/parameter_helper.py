"""Helper module for error handling during AzureParameter object creation."""
from mc_nag.base_utils.exceptions import InvalidParameter


def check_params_type(parameters):
    """Checks that parameters within the template all have the required 'type' keys."""
    missing_param_required_keys = []
    for key, value in parameters.items():
        if 'type' not in value:
            missing_param_required_keys.append(key)
    if len(missing_param_required_keys) > 0:
        raise InvalidParameter("Error - The following template parameters are missing the "
                               f"required 'type' key: \n {missing_param_required_keys}")


def check_template_params_default_value(parameters):
    """Checks that the parameters within a template all have the 'defaultValue' keys.

    This only runs this check when a parameters JSON file is not being passed in.
    """
    missing_param_required_keys = []
    for key, value in parameters.items():
        if 'defaultValue' not in value:
            missing_param_required_keys.append(key)
    if len(missing_param_required_keys) > 0:
        raise InvalidParameter("Error - The following template parameters are missing "
                               f"'defaultValue' keys and are not being passed in as part "
                               f"of a parameters JSON file: \n {missing_param_required_keys}")


def check_file_params_value(file_parameters):
    """Validates the parameters in a parameters JSON file.

    This checks that all of the parameters inside a parameters JSON file contain the required
    'value' keys.
    """
    missing_param_required_keys = []
    for key, value in file_parameters.items():
        if 'value' not in value:
            missing_param_required_keys.append(key)
    if len(missing_param_required_keys) > 0:
        raise InvalidParameter("Error - The following is the list of parameters"
                               " from the passed in parameters JSON file that are missing "
                               f"the required 'value' key: \n {missing_param_required_keys}")


def check_default_value(param_key, param_value):
    """Checks a single template parameter for the 'defaultValue' key.

    This is used to check a single template parameter for the 'defaultValue' key when a parameters
    JSON file is passed in that does include the template parameter.
    """
    if 'defaultValue' not in param_value:
        message = f"Parameter '{param_key}' is missing the 'defaultValue' key inside " \
                  f"the template and was not passed in as part of a " \
                  f"parameters JSON file."
        raise InvalidParameter(message)
