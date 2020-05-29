"""
Builtin commands.
"""

import os
import re

from .utils import ditzcmd


class CmdBuiltin(object):
    @ditzcmd
    def do_init(self, args):
        """
        Command:
           init -- Initialize a database for a new project

        Usage:
           init
        """

        # This is a no-op, kept for Ditz compatibility, since
        # initialization is automatically done if no database exists.
        self.write("Issue database already set up in", self.db.issuedir)

    @ditzcmd
    def do_reconfigure(self, args):
        """
        Command:
           reconfigure -- Rerun configuration script

        Usage:
           reconfigure
        """

        self.setup(self.db.config)

    @ditzcmd
    def do_cmds(self, args):
        """
        Command:
           cmds -- List matching commands

        Usage:
           cmds [REGEXP]
        """

        regexp = self.getregexp(args.REGEXP)

        for name in sorted(set(self.commands)):
            if "_" in name:
                continue

            meth = getattr(self, "do_" + name)
            doc = meth.__doc__
            match = re.match(r"Command.*\n\s*(.+ -- .+)", doc, re.M)
            if match:
                text = match.group(1)
                if regexp.search(text):
                    self.write(text)

    @ditzcmd
    def do_ipython(self, args):
        """
        Command:
           ipython -- Enter embedded IPython interpreter

        Usage:
           ipython
        """

        try:
            from IPython import embed
        except ImportError:
            self.error("IPython is not available")

        embed()

    @ditzcmd
    def do_shell(self, args):
        """
        Command:
           shell -- run a system command

        Usage:
           shell [ARG...]
        """

        os.system(" ".join(args.ARG))

    @ditzcmd
    def do_quit(self, args):
        """
        Command:
           quit -- Quit the interactive command loop

        Usage:
           quit
        """

        return True

    do_EOF = do_quit
