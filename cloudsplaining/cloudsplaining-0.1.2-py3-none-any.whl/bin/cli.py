#! /usr/bin/env python
# Copyright (c) 2020, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
"""
    Cloudsplaining is an AWS IAM Assessment tool that identifies violations of least privilege and generates a risk-prioritized HTML report with a triage worksheet.
"""
# __version__ = "0.1.2"
import click
from cloudsplaining import command
from cloudsplaining.bin.version import __version__


@click.group()
@click.version_option(version=__version__)
def cloudsplaining():
    """
    Cloudsplaining is an AWS IAM Assessment tool that identifies violations of least privilege and generates a risk-prioritized HTML report with a triage worksheet.
    """


cloudsplaining.add_command(command.create_exclusions_file.create_exclusions_file)
cloudsplaining.add_command(command.expand_policy.expand_policy)
cloudsplaining.add_command(command.scan.scan)
cloudsplaining.add_command(command.scan_policy_file.scan_policy_file)
cloudsplaining.add_command(command.download.download)


def main():
    """Cloudsplaining is an AWS IAM Assessment tool that identifies violations of least privilege and generates a risk-prioritized HTML report with a triage worksheet."""
    cloudsplaining()


if __name__ == "__main__":
    cloudsplaining()
