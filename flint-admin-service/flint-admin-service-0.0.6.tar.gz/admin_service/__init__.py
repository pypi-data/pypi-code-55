from .version import __version__
from .admin import create_app

# if somebody does "from admin_service import *", this is what they will
# be able to access:
__all__ = [
    'create_app',
]
