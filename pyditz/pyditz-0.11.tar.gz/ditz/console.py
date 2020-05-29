"""
Main console program.
"""

from __future__ import print_function

import os
import sys

from .config import config, config_path
from .logger import init_logging
from .docopt import docoptions

from . import __version__

# Name of the main program.
PROGRAM = "pyditz"

# Version string.
VERSION = "%s %s" % (PROGRAM, __version__)

# Usage string.
USAGE = """
Usage: {prog} [options] [COMMAND] [ARG...]
       {prog} (-h | --help)
       {prog} --version

Arguments:
  COMMAND               Subcommand to run
  ARG                   Arguments to pass to subcommand

Issue database options:
  -i DIR, --issuedir DIR
                        Use the given issue directory

Feature options:
  -S, --no-search       Turn off searching of parent directories
  -P, --no-pager        Turn off paging of output
  -H, --no-highlight    Turn off syntax highlighting
  -N, --no-setup        Turn off interactive setup
  -X, --no-plugins      Turn off loading of external plugins
  -V, --no-vcs          Turn off use of version control

Configuration options:
  -u FILE, --userconfig FILE
                        Use the given user config file
  -c OPT[,OPT...], --config OPT[,OPT...]
                        Set one or more config options explicitly

Information-only options:
  -p, --path            Show path information
  -s, --schemas         Show data validation schemas
  -h, --help            Show this help message
  --version             Show program's version number

Other options:
  -v, --verbose         Be verbose about things
  -t, --trace           Print traceback on error
"""


def main(args=sys.argv[1:]):
    # Prepend arguments from environment, if any.
    flags = os.environ.get("DITZFLAGS", "")
    args = flags.split() + args

    # Parse arguments.
    usage = USAGE.format(prog=os.path.basename(sys.argv[0]))
    opts = docoptions(usage, argv=args, version=VERSION, options_first=True)

    try:
        # Initialise.
        init_logging(opts.verbose)

        if opts.userconfig:
            config.set_file(opts.userconfig)

        if opts.config:
            for setting in opts.config.split(","):
                config.set_option(setting)

        issuedir = opts.issuedir or "."

        # Do what's required.
        if opts.path:
            show_path_info(issuedir)
        elif opts.schemas:
            show_schemas()
        else:
            run_commands(opts, issuedir)

    except KeyboardInterrupt:
        if opts.trace:
            raise
        else:
            print()
            sys.exit("%s: aborted" % PROGRAM)

    except Exception as msg:
        if opts.trace:
            raise
        else:
            sys.exit("%s: error: %s" % (PROGRAM, msg))


def run_commands(opts, issuedir):
    """
    Run a single command or enter command loop.
    """

    from .plugin import loader
    from .settings import Settings
    from .util import terminal_size

    # Build common settings to pass to Ditz command.
    settings = Settings(autosave=True, usecache=True)

    if opts.no_highlight:
        settings.highlight = False
    else:
        settings.highlight = config.getboolean('highlight', 'enable')

    if opts.no_vcs:
        settings.versioncontrol = False
    else:
        settings.versioncontrol = config.getboolean('vcs', 'enable')

    cols, lines = terminal_size()
    settings.termlines = 0 if opts.no_pager else lines
    settings.termcols = cols

    settings.externalplugins = not opts.no_plugins
    settings.searchparents = not opts.no_search
    settings.setup = not opts.no_setup

    # Set up plugin load paths.
    if settings.externalplugins:
        # Load plugins from user config directory.
        path = config_path("plugins")
        loader.add_path(path)

        # Load setuptools plugins.
        loader.add_entrypoint('ditz.plugin')

    # Load plugins.
    loader.load()

    # Run things.
    from .commands import DitzCmd

    if not opts.COMMAND:
        cmd = DitzCmd(issuedir, settings=settings, interactive=True)
        cmd.cmdloop()
    else:
        cmd = DitzCmd(issuedir, settings=settings)
        command = opts.COMMAND + " " + " ".join(opts.ARG)
        cmd.onecmd(command)
        if not cmd.success:
            sys.exit(1)


def show_path_info(issuedir):
    """
    Show path information.
    """

    from .objects import Project, Config

    repopath, conf = Config.find(issuedir, error=True)
    issuepath = os.path.join(repopath, conf.issue_dir)
    projectpath = os.path.join(issuepath, Project.filename)

    print("repo:", repopath)
    print("issues:", issuepath)
    print("project:", projectpath)


def show_schemas():
    """
    Show data validation schemas.
    """

    import json
    from . import schemas

    data = {'issue': schemas.issue,
            'release': schemas.release,
            'component': schemas.component,
            'project': schemas.project}

    output = json.dumps(data, indent=4, separators=(',', ': '),
                        default=lambda o: "function")

    print(output)


if __name__ == "__main__":
    main()
