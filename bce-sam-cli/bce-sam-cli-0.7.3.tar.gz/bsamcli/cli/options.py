"""
This file contains common CLI options common to all commands. As we add more commands, this will
become a repository of options that other commands could use when needed.
"""

import click

from .context import Context


def debug_option(f):
    """
    Configures --debug option for CLI

    :param f: Callback Function to be passed to Click
    """
    def callback(ctx, param, value):
        state = ctx.ensure_object(Context)
        state.debug = value
        return value

    return click.option('--debug',
                        expose_value=False,
                        is_flag=True,
                        envvar="SAM_DEBUG",
                        help='Turn on debug logging to print debug message generated by SAM CLI.',
                        callback=callback)(f)


def region_option(f):
    """
    Configures --region option for CLI

    :param f: Callback Function to be passed to Click
    """
    def callback(ctx, param, value):
        state = ctx.ensure_object(Context)
        state.region = value
        return value

    return click.option('--region',
                        expose_value=False,
                        help='Set the BCE Region of the service (e.g. bj).',
                        callback=callback)(f)


def profile_option(f):
    """
    Configures --profile option for CLI

    :param f: Callback Function to be passed to Click
    """
    def callback(ctx, param, value):
        state = ctx.ensure_object(Context)
        state.profile = value
        return value

    return click.option('--profile',
                        expose_value=False,
                        help='Select a specific profile from your credential file to get BCE credentials.',
                        callback=callback)(f)
