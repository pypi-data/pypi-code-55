__version__ = '0.0.7'
__author__ = 'Mike Kroutikov'
__author_email__ = 'pgmmpk@gmail.com'


from .api import (
    Config,
    ls,
    register,
    push,
    pull,
    purge,
    dataset,
)

from .dataset import Dataset