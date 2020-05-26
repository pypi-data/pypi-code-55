"""Report and Output generator helper."""

import os
import sys
from mc_nag.base_utils.rule_evaluator import RuleEvaluator
from mc_nag.base_utils.printers import OutputPrinter, BCOLORS
from azure_nag.models.azure_template import AzureTemplate


def process_templates(filepath, paramfile=None):
    """Processes templates in provided file path."""
    azure_template_models = []
    if os.path.isdir(filepath):
        for root, _, files in os.walk(filepath):
            for file in files:
                azure_template_models.append(AzureTemplate(f'{root}/{file}'))
    else:
        azure_template_models.append(AzureTemplate(filepath, paramfile))
    return azure_template_models


def report_violations(azure_template_models,
                      output,
                      rule_dir_manager,
                      rule_param,
                      enable_tags_only,
                      verbose=0):
    """Helps generate output report from violations."""
    error_violation_counts = 0
    rules_evaluated = []
    for atm in azure_template_models:
        # Instantiate RuleEvaluator and evaluate rules
        rule_evaluator = RuleEvaluator(atm,
                                       rule_dir_manager,
                                       rule_param,
                                       enable_tags_only)
        violations_dict, violations_counts, rules = rule_evaluator.evaluate_rules()
        error_violation_counts += violations_counts.get('ERROR', 0)
        for rule in rules:
            rules_evaluated.append(rule)
        # Print violations in plain text
        print('')
        print(f'-- Template Evaluated: {atm.template_path} --')
        if verbose > 0:
            print(atm)
        getattr(OutputPrinter, output)(violations_dict, violations_counts, rules)
        print()

    if error_violation_counts > 0:
        print_total_report_and_rules(rules_evaluated)
        sys.exit(f'- {BCOLORS["ERROR"]}Total Error Violations{BCOLORS["ENDC"]}: '
                 f'{error_violation_counts}')
    else:
        sys.exit(0)


def print_total_report_and_rules(rules_evaluated):
    """Prints final portion of output with total error violations and rules evaluated."""
    rule_set = [rule.__name__ for rule in sorted(rules_evaluated,
                                                 key=lambda x: x.__name__)]
    print(''.rjust(34, '='))
    print(f'{BCOLORS["UNDERLINE"]}{BCOLORS["HEADER"]}FINAL REPORT{BCOLORS["ENDC"]}')
    print()
    print(f'- {BCOLORS["CYAN"]}Rules Evaluated{BCOLORS["ENDC"]}:')
    for rule in set(rule_set):
        print(f'   {rule}')
    print()
