"""Model implementation.
"""
from __future__ import annotations
from typing import Dict, Any, Optional
from .client import Client

class BaseAPI():
    """Class definition for the model class.
    """

    client = Client()

    def __init__(self,
                 attrs: Optional[Dict[str, Any]] = None,
                 client: Optional[Client] = None):
        """Initiate the model with the client and the attributes.
        """
        if client:
            self.client = client

        self.attrs = attrs

    def summarize(self) -> str:
        """Summarize this object.
        """
        return str(self.attrs)
