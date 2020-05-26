"""Azure Resource Object Class."""


class AzureResource:
    """Creates Azure Resource Object."""

    def __init__(self, resource_type, resource_name, properties,
                 raw_string, line_number):
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.properties = properties
        self.raw_string = raw_string
        self.line_number = line_number
