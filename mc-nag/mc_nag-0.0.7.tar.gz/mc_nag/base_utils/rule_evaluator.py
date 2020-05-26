"""Utility functions related to rule evaluation."""

import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from itertools import chain
from tabulate import tabulate

from mc_nag.base_utils.exceptions import InvalidParameter
from mc_nag.base_utils.models.rule_directory import RuleDirectoryManager
from .printers import BCOLORS

TABULATE_FORMAT = 'fancy_grid'


class RuleEvaluator:
    """Engine to evaluate rules.

    This class will find all rules inside the supplied standard rules
    directory and evaluate them against the given template model.

    :param model: Template data model built from a template.
    :param rule_dir_manager: Required to pass an instance of the RuleDirectoryManager.
    :param requested_tags: Optional tuple of tags to filter Rules.
    """

    def __init__(self, model: str, rule_dir_manager: RuleDirectoryManager,
                 rule_params=None, requested_tags: tuple = None):
        """Assign arguments as attributes and prepare rules."""
        self.model = model
        try:
            self.rule_dir_manager = rule_dir_manager
        except AttributeError:
            raise InvalidParameter(
                "RuleEvaluator must be pass an instance of RuleDirectoryManager.")
        self.requested_tags = set()
        self._set_requested_tags(requested_tags)
        self.rule_set = self._retrieve_rule_objects()
        self.rule_params = rule_params

    def _set_requested_tags(self, requested_tags):
        if isinstance(requested_tags, str):
            self.requested_tags.update([requested_tags])
        if isinstance(requested_tags, (list, tuple)):
            self.requested_tags.update(requested_tags)

    def evaluate_rules(self):
        """Evaluate given rules against the data model."""
        violations_by_rule = {}
        severity_counts = {}

        # Allows tag-based Rule scanning.
        if self.requested_tags:
            rule_classes = self._filter_tags()
        else:
            rule_classes = self.rule_set

        for rule in rule_classes:
            # Instantiate rule
            rule_object = rule(self.model, self.rule_params)

            # Evaluate rule
            violating_resources = rule_object.evaluate()

            # Continue to next rule if no violations found
            if not violating_resources:
                continue

            # Add to violations by rule
            if rule not in violations_by_rule:
                violations_by_rule[rule] = []
            violations_by_rule[rule] += violating_resources

            # Add to severity counter
            if rule_object.severity not in severity_counts:
                severity_counts[rule_object.severity] = 0
            severity_counts[rule_object.severity] += 1

        return violations_by_rule, severity_counts, self.rule_set

    def display_rules(self):
        """Output list of rules and rule IDs in given format.

        :param output: Format in which the output should be.
        """
        if not self.rule_set:
            return None

        # Dict to hold values for duplicate checking
        dupe_rules = []
        rev_dict = {}

        # Instantiate rules to validate base structural requirements
        for rule in self.rule_set:
            _ = rule(None)

        # Sort rules by ID
        sorted_rules = sorted(self.rule_set, key=lambda x: x.rule_id)

        # Gather table information & print
        print(
            tabulate(
                [[rule.rule_id, rule.__name__] for rule in sorted_rules],
                headers=["Rule ID", "Rule Name"],
                tablefmt=TABULATE_FORMAT
            )
        )

        # Find duplicate rule IDs
        for rule in sorted_rules:
            rev_dict.setdefault(rule.rule_id, set()).add(
                f'{rule.__name__} ({rule.__module__}.py)'
            )
        for key, values in rev_dict.items():
            if len(values) > 1:
                for value in values:
                    dupe_rules.append([key, value])

        # Output
        if dupe_rules:
            print(f'\n{BCOLORS["ERROR"]}Found duplicate rule IDs!' +  # noqa: W504
                  f'{BCOLORS["ENDC"]}\n')

            print(tabulate(dupe_rules, headers=["Duplicate Rule ID", "Duplicate Rule Names"],
                           tablefmt=TABULATE_FORMAT)
                  )
        else:
            print(f'\n{BCOLORS["OKGREEN"]}No duplicates{BCOLORS["ENDC"]} 🎉')

        return dupe_rules

    def _retrieve_rule_objects(self):
        """Return list of rule classes to evaluate.

        Based on this StackOverflow info:
        https://stackoverflow.com/a/41904558
        """
        try:
            paths = self.rule_dir_manager.rule_directories()
        except AttributeError:
            raise InvalidParameter("RuleEvaluator requires the `rule_dir_manager` parameter.")
        # Set to hold found rules
        rules = set()
        found_rule_modules = set()

        # Iterate over all rules paths (standard and custom)
        for path, _, files in chain.from_iterable(os.walk(path)
                                                  for path in paths):
            # Iterate over .py files in path
            for py_file in [f[:-3] for f in files
                            if f.endswith('.py') and f != '__init__.py']:
                # Prepare module path to import
                module_path = f'{path}/{py_file}.py'

                # Import .py file as a module
                spec = spec_from_file_location(py_file, module_path)
                mod = module_from_spec(spec)
                spec.loader.exec_module(mod)

                # Retrieve list of classes from module
                classes = [getattr(mod, x) for x in dir(mod)
                           if isinstance(getattr(mod, x), type) and  # noqa: W504
                           not hasattr(getattr(mod, x), f'_{x}__exclude_from_evaluation')]

                # Set new found class names as part of the system modules
                for cls in classes:
                    setattr(sys.modules[__name__], cls.__name__, cls)

                # Add new found classes to rules set
                if py_file not in found_rule_modules:
                    rules.update(classes)
                    found_rule_modules.add(py_file)

        return rules

    def display_tags(self):
        """Gather tags from the rule set & print."""
        categories = set()
        sources = set()
        for rule in self.rule_set:
            # Category Tags:
            try:
                categories.update(rule.category_tags)
            except AttributeError:
                pass
            # Resource Tags:
            try:
                sources.update(rule.source_tags)
            except AttributeError:
                pass

        if categories or sources:
            print(f'\n{BCOLORS["ERROR"]}List of Tags{BCOLORS["ENDC"]}\n')
            if categories:
                category_list = [[x] for x in categories]
                print(tabulate(category_list, headers=["Category Tags"],
                               tablefmt=TABULATE_FORMAT)
                      )
            if sources:
                resource_list = [[x] for x in sources]
                print(tabulate(resource_list, headers=["Source Tags"],
                               tablefmt=TABULATE_FORMAT)
                      )
        else:
            print(f'\n{BCOLORS["OKGREEN"]}No tags for your rule set.{BCOLORS["ENDC"]}')

    def _filter_tags(self):
        """Find only Rules with matching tags.

        :return result:Returns a set of tag filtered Rule classes.
        """
        result = set()
        for rule in self.rule_set:
            all_tags_of_rule = rule.source_tags.union(rule.category_tags)
            if all_tags_of_rule.intersection(self.requested_tags):
                result.add(rule)
        return result
