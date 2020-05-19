# flake8: noqa
"""
Module for Moic fun commands
"""
import click

from moic.cli import console, logger


@click.command()
def rabbit():
    """
    Print an amazing rabbit: Tribute to @fattibenji https://github.com/fattybenji
    """
    logger.debug("Execute 'rabbit' command")
    funny_rabbit = """
              /|      __
             / |   ,-~ /
            Y :|  //  /
            | jj /( .^
             >-"~"-v"
            /       Y
           jo  o    |
          ( ~T~     j    Hello !
           >._-' _./
          /   "~"  |
         Y     _,  |
        /| ;-"~ _  l
       / l/ ,-"~    \\
       \//\/      .- \\
        Y        /    Y
        l       I     !
        ]\      _\    /"\\
       (" ~----( ~   Y.  )
    """

    console.print(funny_rabbit)
