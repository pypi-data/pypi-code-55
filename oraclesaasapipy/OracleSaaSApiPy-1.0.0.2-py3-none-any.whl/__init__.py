"""A simple lightweight API to interact with Oracle ERP integration Service.

Usage:
    >>> import OracleSaaSApi
    >>> erp = OracleSaaSApi.ErpServiceApi(url, username, password)
    >>> docId = erp.upload_file_to_ucm()

"""

__all__ = ['ErpServiceApi', 'ErpServiceApiResponse', 'utils', 'constants', 'api']

# metadata
__author__ = 'Pratik Munot'
__version__ = '1.0.0'

# imports
from .api import ErpServiceApi, ErpServiceApiResponse
from . import utils, constants, api
