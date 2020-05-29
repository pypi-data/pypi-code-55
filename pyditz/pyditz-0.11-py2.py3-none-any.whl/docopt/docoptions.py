"""
Docopt wrapper allowing options as attributes.
"""

import re
from functools import partial

from .docopt import docopt
from .doccmd import docopt_cmd


class docoptions(object):
    """
    Docopt front end allowing options as attributes.
    """

    def __init__(self, *args, **kw):
        self._docopt = docopt(*args, **kw)
        for opt, value in self._docopt.items():
            attr = re.sub(r'^-+', '', opt).replace('-', '_')
            setattr(self, attr, value)

    def __repr__(self):
        args = ["%s=%r" % elt for elt in sorted(self._docopt.items())]
        return "<docopt: %s>" % " ".join(args)


docoptions_cmd = partial(docopt_cmd, docfunc=docoptions)
