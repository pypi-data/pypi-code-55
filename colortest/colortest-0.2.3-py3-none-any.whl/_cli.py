from __future__ import division

import click

from colortest import __version__


s = "/\\/\\/\\/\\/\\"


@click.command()
@click.option("--width", default=76, help="the width of the output")
@click.version_option(prog_name="colortest", version=__version__)
def main(width):
    """
    Ported from https://gist.github.com/XVilka/8346728.
    """

    for column in range(width + 1):
        red = 255 - (column * 255 / width)
        green = column * 510 / width
        blue = column * 255 / width

        if green > 255:
            green = 510 - green

        click.echo("\033[48;2;%d;%d;%dm" % (red, green, blue), nl=False)
        click.echo(
            "\033[38;2;%d;%d;%dm" % (255 - red, 255 - green, 255 - blue),
            nl=False,
        )
        click.echo("%s\033[0m" % (s[(column + 1) % len(s)],), nl=False)
    click.echo()
