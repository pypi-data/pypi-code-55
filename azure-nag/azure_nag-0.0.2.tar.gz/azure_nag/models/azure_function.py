"""Azure Function Object Class."""


class AzureFunction:
    """Creates Azure Function Object."""

    def __init__(self, function_namespace, function_members):
        self.function_namespace = function_namespace
        self.function_members = function_members
