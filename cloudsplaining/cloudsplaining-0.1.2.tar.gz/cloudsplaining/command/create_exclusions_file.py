"""
Create YML Template files for the exclusions template command.
This way, users don't have to remember exactly how to phrase the yaml files, since this command creates it for them.
"""
# Copyright (c) 2020, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
import os
from pathlib import Path
import logging
import click
import click_log
from cloudsplaining.shared.constants import EXCLUSIONS_TEMPLATE

logger = logging.getLogger()
click_log.basic_config(logger)


@click.command(
    context_settings=dict(max_content_width=160),
    short_help="Creates a YML file to be used as a custom exclusions template",
)
@click.option(
    "--output-file",
    type=click.Path(exists=False),
    default=os.path.join(os.getcwd(), "exclusions.yml"),
    required=True,
    help="Relative path to output file where we want to store the exclusions template.",
)
@click_log.simple_verbosity_option(logger)
def create_exclusions_file(output_file):
    """
    Creates a YML file to be used as a custom exclusions template,
    so users can fill out the fields without needing to look up the required format.
    """

    filename = Path(output_file).resolve()
    with open(filename, "a") as file_obj:
        for line in EXCLUSIONS_TEMPLATE:
            file_obj.write(line)
    print(f"Exclusions template file written to: {filename}")
    print(
        "Make sure you download your account authorization details before running the scan. Set your AWS access keys as environment variables then run: "
    )
    print("\tcloudsplaining download")
    print("You can use this with the scan command as shown below: ")
    print("\tcloudsplaining scan --exclusions-file exclusions.yml --input default.json")
