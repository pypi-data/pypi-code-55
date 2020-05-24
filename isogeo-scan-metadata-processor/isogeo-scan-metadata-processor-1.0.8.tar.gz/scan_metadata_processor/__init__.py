#! python3  # noqa: E265

import warnings

# submodules
from .__about__ import __version__  # noqa: F401

# subpackages
from .parser import Listing, Lookup, Sign  # noqa: F401
from .converter import (  # noqa: F401
    MATCHER_FORMAT,
    MATCHER_GEOMETRY,
    LookupToIsogeo,
    match_coordinate_system,
)
from .parser import MetadataJsonReader, Unzipper  # noqa: F401

# must be imported at last
from .database.isogeo import MetadataSynchronizer  # noqa: F401

# conditional import
try:
    from elasticsearch import Elasticsearch  # noqa: F401

    ES_ENABLED = True
    from .database import ElasticSearchManager  # noqa: F401
except ImportError:
    ES_ENABLED = False
    warnings.warn(
        message="ElasticSearch package is not installed. Related functions cannot be used.",
        category=ImportWarning,
    )
