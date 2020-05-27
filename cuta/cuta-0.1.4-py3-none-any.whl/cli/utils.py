
from emoji import emojize
import sys
import typer

import cuta


_color = None


def get_color():
    return _color


def set_color(color):
    global _color
    _color = color


def echo(*args, **kwargs):
    text = fmt(*args, **kwargs)
    typer.echo(text)


def fmt(msg, color=None, emoji=None, **options):
    color = color or get_color()
    if color or options:
        msg = typer.style(msg, fg=color, **options)

    if emoji:
        msg = emojize(f":{emoji}: {msg}", use_aliases=True)

    return msg


def version():
    msg = f"Cuta: {cuta.version}"
    echo(msg, color=typer.colors.BRIGHT_WHITE, bold=True)


def title(title, color=None, emoji=None):
    echo("-" * 72, color=color)
    echo(title, color=color, emoji=emoji)
    echo("-" * 72, color=color)


def complete(msg="Complete!"):
    echo(msg, color=typer.colors.BRIGHT_WHITE, bold=True)


def clear_lines(count=1):
    for index in range(count):
        sys.stdout.write("\x1b[1A\x1b[2K")
