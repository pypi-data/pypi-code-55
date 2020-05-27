from pkg_resources import get_distribution, DistributionNotFound

from .appen import AppenClient, AppenJob
from . import appen, exceptions

try:
    __version__ = get_distribution("py-appen").version
except DistributionNotFound:
    pass


__all__ = [
    AppenJob,
    AppenClient,
    appen,
    exceptions,
    __version__
]
