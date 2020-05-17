# coding: utf-8

"""Module that contains some neat functions to print nice things to terminal.
"""

from typing import List, TextIO

from enum import Enum
from sys import (stdout as STDOUT, stderr as STDERR)
from termcolor import colored  # pylint: disable=import-error

__all__ = [
    "Color",
    "prettyprint",
    "printinfo",
    "printwarning",
    "printerror",
    "printstatus"
]

G_QUIET = False


class Color(Enum):
    GREY = "grey"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"


def prettyprint(text: str, color=Color.WHITE, out=STDOUT, bold=False, dark=False,
                underline=False, blink=False, indent=0, end='\n'):
    """Awesome print.

    Args:
        text (str): your text
        color (Color, optional): color of the text. Default is white.
        out (TextIO, optional): output. Default is stdout.
        bold (bool, optional): print bold text. Default is False.
        dark (bool, optional): print dark text. Default is False.
        underline (bool, optional): underline text. Default is False.
        blink (bool, optional): the text blinks. Default is False.
        indent (int, optional): indentation level. Default is 0. Increase by 2 spaces for each level.
        end (str, optional): end - same as for standard print function. Default is '\n'.
    """
    if G_QUIET:
        return

    attrs: List[str] = []
    if bold:
        attrs.append("bold")
    if dark:
        attrs.append("dark")
    if underline:
        attrs.append("underline")
    if blink:
        attrs.append("blink")

    print(f"{' ' * 2 * indent}", file=out, end='')
    print(colored(text, color.value, attrs=attrs), file=out, end=end)


def printinfo(text: str, bold=False, indent=0, end='\n'):
    """Shortcut to print "info" messages.

    See prettyprint.
    """
    if G_QUIET:
        return

    prettyprint(text, Color.WHITE, STDOUT, bold=bold, indent=indent, end=end)


def printwarning(text: str, bold=False, indent=0, end='\n'):
    """Shortcut to print "warning" messages.

    See prettyprint.
    """
    if G_QUIET:
        return

    prettyprint(text, Color.YELLOW, STDOUT, bold=bold, indent=indent, end=end)


def printerror(text: str, indent=0, end='\n'):
    """Shortcut to print "error" messages.

    See prettyprint.
    """
    if G_QUIET:
        return

    prettyprint(text, Color.RED, STDERR, indent=indent, end=end)


def printstatus(status: str, indent=0, end='\n'):
    """Shortcut to print Test or Testcase status.

    See prettyprint.
    """
    if G_QUIET:
        return

    if (status == "Passed"):
        color = Color.GREEN
    elif (status == "Failed"):
        color = Color.RED
    elif (status == "Timed out"):
        color = Color.MAGENTA
    elif (status == "Skipped"):
        color = Color.YELLOW
    else:
        color = Color.GREY

    prettyprint(f"{status}", color, bold=True, indent=indent, end=end)
