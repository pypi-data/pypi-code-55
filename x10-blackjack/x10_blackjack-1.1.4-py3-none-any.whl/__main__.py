#!/usr/bin/env python3
"""
Sub-module defining the default "entrypoint" when program is executed as a python module.

Ref;
- `python -m blackjack` if it's installed into the `PYTHONPATH`,
- or `python -m blackjack/` if you're referencing local folder inside of git repo.
"""

# Imports of module(s) internal to this project/package
from blackjack.cli import cli


if __name__ == '__main__':
    # Just pass on to the cli-function in the
    # 'blackjack/cli.py' file, and let it be the 'main()' function.
    cli()
