"""Utilities for authentication."""

from typing import Any, Mapping, Optional, Type

from ._auth import Auth
from ._auth0 import AUTH0_AUTH_TYPE, Auth0Authentication
from ._auth_basic import BASIC_AUTH_TYPE, BasicAuthentication
from .parsing import ConfigParsingError

_AUTH_CLASSES = [Auth0Authentication, BasicAuthentication]


def get_type(auth_type: str) -> Type:
    """Get the type."""
    auth_classes = {
        BASIC_AUTH_TYPE: BasicAuthentication,
        AUTH0_AUTH_TYPE: Auth0Authentication,
    }
    if auth_type in auth_classes:
        return auth_classes[auth_type]
    raise KeyError("Authentication type {auth_type} is not supported")


def parse_auth(data: Mapping[str, Any]) -> Auth:
    """Parse the authentication."""
    if len(data) > 1:
        raise ConfigParsingError("Only one authentication can be used.")
    if "auth0" in data:
        return Auth0Authentication._from_dict(data["auth0"])
    if "basic" in data:
        return BasicAuthentication._from_dict(data["basic"])
    raise ConfigParsingError("Supported authentication are basic and auth0")


def merge_auth(instance1: Optional[Auth], instance2: Optional[Auth]) -> Optional[Auth]:
    """Merge the authentitation."""
    if instance1 is None:
        return instance2
    if instance2 is None:
        return instance1
    for clazz in _AUTH_CLASSES:
        if isinstance(instance1, clazz) and isinstance(instance2, clazz):
            return clazz._do_merge(instance1, instance2)
    # If they have different types we cannot merge
    return instance2
