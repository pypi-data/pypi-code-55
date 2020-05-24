"""
This package provides client for Ucal Manager Server, open source software for
nanocalorimetry - https://bitbucket.org/zimka_b/ucal_manager/.

Two most important parts of this package are UcalClient and UcalBlock.
Their docs describe the model of interaction between client and server.
"""
from .base import UcalBlock, UcalState, UcalConfig, UcalTs
from .client import UcalClient
