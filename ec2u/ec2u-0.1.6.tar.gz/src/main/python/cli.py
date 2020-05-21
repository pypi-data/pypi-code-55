import click
from ec2_metadata import ec2_metadata
from . import ec2
import sys
import logging
from pathlib import Path
import os


__VERSION__ = "0.1.6"


@click.group()
@click.option("--verbose", is_flag=True)
@click.version_option(__VERSION__)
def main(verbose):
    logger = logging.getLogger()
    level = "INFO"
    if verbose:
        level = "DEBUG"
    logger.setLevel(level)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


@main.command(short_help="Check whether or not instance has given tag")
@click.option("-id", "--instance-id", default="", help="ID of instance. The option can be omitted if run on EC2 instance")
@click.option("-k", "--tag-key", "--key")
@click.option("-v", "--tag-value", "--value", multiple=True, help="Can be specified multiple values")
@click.option("--verbose", is_flag=True)
def has_tag(instance_id, tag_key, tag_value, verbose):
    if verbose:
        logging.getLogger().setLevel("DEBUG")
    if instance_id == "":
        instance_id = ec2_metadata.instance_id
    has_tag = ec2.has_tags(instance_id, tag_key, tag_value)
    if has_tag:
        logging.info("The instance has no tag that match the given tag")
        sys.exit(1)
    logging.info("The instance has tag that match the given tag")


@main.command(short_help="Generate AWS configuration file")
@click.option("--verbose", is_flag=True)
def gen_config(verbose):
    if verbose:
        logging.getLogger().setLevel("DEBUG")
    config = \
        """\
[default]
region = %s
""" % ec2_metadata.region
    file_path = "%s/.aws/credentials" % str(Path.home())
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file=file_path, mode="w") as f:
        f.write(config)
    logging.info(
        "Configuration has been successfully generated at %s" % file_path)


@main.command(short_help="Get private IPv4 of the instance")
@click.option("--verbose", is_flag=True)
def private_ipv4(verbose):
    if verbose:
        logging.getLogger().setLevel("DEBUG")
    click.echo(ec2_metadata.private_ipv4)
