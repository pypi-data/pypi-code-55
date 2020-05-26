"""Printers for outputing results in different formats."""

from json import dumps as json_dumps
from yaml import dump as yaml_dump


BCOLORS = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'ERROR': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'CYAN': '\033[96m'
}


class OutputPrinter:
    """Helper class to output violations data in different formats.

    Each method is a static method that accepts the following params:
    :param violations: Dictionary of all violations, keyed by rule object.
    :param counts: Dictionary of counts of violations by severity.
    :param rules: List of rules evaluated against the templates.
    """

    @staticmethod
    def none(*unused):
        """Silence output."""

    @staticmethod
    def json(violations, counts, rules=None):
        """Output aggreagted information in JSON format.

        :param violations: Dict of all violations found keyed by a tuple of
                        (rule_name, rule_id).
        :param counts: Dict of counts of violations keyed by severity.
        :param rules: List of rules evaluated against the templates.
        """
        print(json_dumps(OutputPrinter._build_output(violations, counts, rules)))

    @staticmethod
    def yaml(violations, counts, rules=None):
        """Output aggreagted information in YAML format.

        :param violations: Dict of all violations found keyed by a tuple of
                           (rule_name, rule_id).
        :param counts: Dict of counts of violations keyed by severity.
        :param rules: List of rules evaluated against the templates.
        """
        print(yaml_dump(OutputPrinter._build_output(violations, counts, rules)))

    @staticmethod
    def text(violations, counts, _=None):
        """Output aggreagted information in plain text format.

        :param violations: Dict of all violations found keyed by a tuple of
                           (rule_name, rule_id).
        :param counts: Dict of counts of violations keyed by severity.
        :param rules: List of rules evaluated against the templates.
        """
        # Print report if any violations
        if counts:
            left_pad = max([len(severity) for severity in counts])
            right_pad = max([len(str(counts[severity]))
                             for severity in counts])

            # Build rule details output
            for rule, violating_resources in violations.items():
                resources_string = [
                    f'{resource.resource_name} (line: {resource.line_number})'
                    for resource in violating_resources]
                header = f'{BCOLORS[rule.severity]}{rule.__name__} ' + \
                    f'({rule.rule_id}){BCOLORS["ENDC"]}'
                left_margin = BCOLORS[rule.severity] + \
                    '|'.rjust(left_pad + 2, ' ') + BCOLORS['ENDC']
                severity = \
                    f"{BCOLORS[rule.severity]}{rule.severity:{left_pad}}" + \
                    BCOLORS['ENDC']
                print(f"""{severity} : {header}
{left_margin} {rule.description}
{left_margin} {rule.url}
{left_margin}
{left_margin} Violating resources: {resources_string}
{left_margin}
{left_margin} To resolve:""")
                for line in rule.resolution.split('\n'):
                    print(f'{left_margin} {line}')

            print()
            print(
                f'{BCOLORS["UNDERLINE"]}{BCOLORS["HEADER"]}{"Template Report":15}{BCOLORS["ENDC"]}'
            )
            for severity in sorted(counts):
                print(
                    f'- {BCOLORS[severity]}{severity:{left_pad}}{BCOLORS["ENDC"]} :' +  # noqa: W504
                    f' {counts[severity]:{right_pad}}'
                )
        else:
            print(f'{BCOLORS["OKGREEN"]}No violations{BCOLORS["ENDC"]} 🎉')

    @staticmethod
    def _build_output(violations, counts, rules=None):
        """Return data organized into dictionary for output.

        :param violations: Dict of all violations found keyed by a tuple of
                           (rule_name, rule_id).
        :param counts: Dict of counts of violations keyed by severity.
        :param rules: List of rules evaluated against the templates.
        """
        output = {
            'violations': [],
            'report': {
                'rules_evaluated': [rule.__name__ for rule in _sort_rules(rules)],
                'total_rules_evaluated': len(rules),
                'total_violations': 0
            }
        }

        # Build report if any violations
        if counts:
            # Build rule details output
            for rule, violating_resources in violations.items():
                rule_dict = {
                    'name': rule.__name__,
                    'rule_id': rule.rule_id,
                    'severity': rule.severity,
                    'description': rule.description,
                    'url': rule.url,
                    'resolution': rule.resolution,
                    'violating_resources': [
                        resource.__dict__ for resource in violating_resources
                    ]
                }
                output['violations'].append(rule_dict)

            for severity in sorted(counts):
                output['report'][severity] = counts[severity]
                output['report']['total_violations'] += counts[severity]

        return output


def _sort_rules(rules):
    """Return a sorted list of rule names."""
    return sorted(rules, key=lambda x: x.__name__)
