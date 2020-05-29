"""
Command utilities.
"""

from functools import partial
from ditz.docopt import docoptions_cmd


ditzcmd = partial(docoptions_cmd,
                  errfunc=lambda self, msg: self.error(msg))
