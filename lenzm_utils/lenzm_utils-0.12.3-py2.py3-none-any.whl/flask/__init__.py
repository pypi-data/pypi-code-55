"""lenzm_utils.flask - Utils for Flask Projects
"""
import urllib

from . import db_admin, url_converters, url_for_obj, url_update  # noqa

def encodeURIComponent(v):  # noqa match JS capitalization
    """Python implementation of Javascript's encodeURIComponent."""
    return urllib.parse.quote(v, safe='~()*!.\'')
