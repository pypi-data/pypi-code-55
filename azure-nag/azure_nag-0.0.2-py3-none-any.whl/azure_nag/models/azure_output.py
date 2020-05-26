"""Azure Output Object Class."""


class AzureOutput:
    """Creates Azure Output Object."""

    def __init__(self, output_name, output_type, output_value):
        self.output_name = output_name
        self.output_type = output_type
        self.output_value = output_value
