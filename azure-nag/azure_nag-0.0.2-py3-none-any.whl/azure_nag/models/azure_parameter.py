"""Azure Parameter Object Class."""


class AzureParameter:
    """Creates Azure Parameter Object."""

    def __init__(self, parameter_name,
                 parameter_default_value, parameter_type):
        self.parameter_name = parameter_name
        self.parameter_value = parameter_default_value
        self.parameter_type = parameter_type
