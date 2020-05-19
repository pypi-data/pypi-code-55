"""Describe Rule Directory class."""


class RuleDirectoryManager():
    """Provides an interface for rule directories.

    Provides a setter and getter for rule directories.
    """

    def __init__(self, enable_standard_rules, standard_rules_dir, custom_rules_dirs):
        """Set add directories from parameters."""
        self._directories = list()
        if enable_standard_rules:
            self.add_rule_dirs(standard_rules_dir)
        if custom_rules_dirs:
            self.add_rule_dirs(custom_rules_dirs)

    def add_rule_dirs(self, directory_path):
        """Setter for rules directories.

        :attr directory_path: Accepts a string or a list.
        """
        if isinstance(directory_path, str):
            self._directories.append(directory_path)
        if isinstance(directory_path, (list, tuple)):
            self._directories.extend(directory_path)

    def rule_directories(self) -> list:
        """Return a list of rule directories."""
        return self._directories
