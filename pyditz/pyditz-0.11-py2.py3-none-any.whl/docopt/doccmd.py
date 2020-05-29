"""
Add docopt support to Cmd methods.

An enhanced version of the interactive demo from docopt.
"""

import shlex
import inspect
from functools import wraps

from .docopt import docopt, DocoptExit


def docopt_cmd(method, docfunc=docopt, errfunc=None):
    "Decorator for automatic docopt parsing of do_<cmd> methods."

    name = method.__name__
    if not name.startswith('do_'):
        raise DocCmdError("method '%s' is not a Cmd method" % name)

    doc = method.__doc__ = inspect.getdoc(method)

    if doc is None:
        raise DocCmdError("method '%s' has no docstring" % name)

    if not errfunc:
        def errfunc(self, msg):
            self.stdout.write('%s\n' % msg)

    @wraps(method)
    def wrapper(self, arg):
        try:
            argv = shlex.split(arg)
        except ValueError as err:
            return errfunc(self, str(err).lower())

        try:
            args = docfunc(doc, argv)
            return method(self, args)
        except DocoptExit as err:
            return errfunc(self, "invalid command option(s)\n\n" + str(err))
        except SystemExit:
            pass

    return wrapper


class DocCmdError(Exception):
    "DocCmd configuration error."
