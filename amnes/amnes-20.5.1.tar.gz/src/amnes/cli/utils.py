"""This module contains helper classes and functions for the CLI."""

import sys
import traceback as tb
from pathlib import Path

import click
from Pyro5.errors import get_pyro_traceback


def click_traceback(exit_code: int) -> None:  # pragma: no cover
    # Helper exit function excluded from pytest coverage
    """Print exception traceback with click functions to `sys.stderr`.

    Args:
        exit_code (int): If not None, `sys.exit()` is called with the given
                         exit code after printing traceback.
    """
    type_, value, traceback = sys.exc_info()
    click.secho("\n## BEGIN TRACEBACK ##\n", file=sys.stderr, fg="magenta")
    if hasattr(value, "_pyroTraceback"):
        click.secho(
            "".join(get_pyro_traceback(type_, value, traceback)),
            file=sys.stderr,
            fg="bright_red",
        )
    else:
        click.secho(
            f"{tb.format_exc()}", file=sys.stderr, fg="bright_red",
        )
    click.secho("##  END  TRACEBACK ##\n", file=sys.stderr, fg="magenta")
    sys.exit(exit_code)


def amnes_license() -> str:
    """License of AMNES.

    Returns:
        str: License of AMNES.
    """
    module_path = Path(globals()["__file__"]).parent.parent
    with Path(module_path / "LICENSE").open("rt") as textf:
        __license__ = "".join(textf.readlines())
    return __license__


def amnes_thirdparty() -> str:
    """Third-Party Libraries of AMNES.

    Returns:
        str: Third-Party Libraries of AMNES.
    """
    module_path = Path(globals()["__file__"]).parent.parent
    with Path(module_path / "THIRDPARTY").open("rt") as textf:
        __thirdparty__ = "".join(textf.readlines())
    return __thirdparty__
