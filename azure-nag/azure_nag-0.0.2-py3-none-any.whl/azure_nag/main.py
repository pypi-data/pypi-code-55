"""Main module for executing mc-nag."""

import os
import click
from mc_nag.base_utils.rule_evaluator import RuleEvaluator
from mc_nag.base_utils.click_cli import (
    add_click_options,
    MAIN_OPTIONS
)
from mc_nag.base_utils.models.rule_directory import RuleDirectoryManager
from azure_nag.report_helper import process_templates, report_violations

# pylint: disable=too-many-arguments

STANDARD_RULES_DIR = os.path.realpath(
    f'{os.path.dirname(os.path.abspath(__file__))}/rules'
)


@click.pass_context
def list_rules(ctx, rule_dir_manager):
    """Output information about existing rules."""
    rule_evaluator = RuleEvaluator(None, rule_dir_manager)
    ctx.exit(1 if rule_evaluator.display_rules() else 0)


@click.pass_context
def list_tags_cmd(ctx, rule_dir_manager):
    """Show all the tags for all Rules."""
    rule_evaluator = RuleEvaluator(None, rule_dir_manager)
    rule_evaluator.display_tags()
    ctx.exit(0)


@click.pass_context
def enable_tags_only_cmd(ctx, rule_dir_manager):  # pylint:disable=W0613
    """Show all the tags for all Rules."""
    ctx.exit(0)


@click.command()
@add_click_options(MAIN_OPTIONS)
def main(**kwargs):
    """Perform template parsing and rule evaluation."""
    # Validate either --enable-standard-rules is set or a custom platform
    # rules dir is given
    if not (kwargs['enable_standard_rules'] or kwargs['custom_platform_rules_dir']):
        raise click.BadParameter(
            "Either '--enable-standard-rules' must be True or " +  # noqa: W504
            "'--custom-platform-rules-dir' must have a value."
        )
    rule_dir_manager = RuleDirectoryManager(kwargs['enable_standard_rules'],
                                            STANDARD_RULES_DIR,
                                            kwargs['custom_platform_rules_dir'])
    if kwargs['rules']:
        list_rules(rule_dir_manager)  # pylint: disable=no-value-for-parameter

    if kwargs['list_tags']:
        list_tags_cmd(rule_dir_manager)  # pylint: disable=no-value-for-parameter

    # Read raw template into string
    if not kwargs['filepath']:
        raise click.BadParameter(
            "--filepath must be supplied to evaluate rules."
        )
    azure_template_models = process_templates(kwargs['filepath'],
                                              kwargs['paramfile'])

    report_violations(azure_template_models,
                      kwargs['output'],
                      rule_dir_manager,
                      kwargs['rule_param'],
                      kwargs['enable_tags_only'],
                      kwargs['verbose'])


if __name__ == "__main__":
    # execute only if run as a script
    main()  # pylint: disable=E1120
