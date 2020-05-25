"""Auth0 authentication."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Collection, Mapping, Optional

from ._auth import Auth
from ._utils import Mergeable
from .parsing import ConfigParsingError

AUTH0_AUTH_TYPE = "auth0"


@dataclass(frozen=True)
class Auth0Authentication(Auth, Mergeable):
    """Auth0 authentication."""

    issuer: Optional[str] = None
    audience: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    role_mapping: Mapping[str, Collection[str]] = field(default_factory=dict)

    @property
    def _type(self):
        return AUTH0_AUTH_TYPE

    @classmethod
    def _from_dict(cls, data: dict):  # noqa
        issuer = data.get("issuer")
        audience = data.get("audience")
        client_id = data.get("client_id")
        client_secret = data.get("client_secret")
        if "role_mapping" not in data:
            raise ConfigParsingError(
                "Auth0 authentication must specify some roles", data
            )
        role_mapping = data["role_mapping"]
        if not isinstance(role_mapping, dict):
            raise ConfigParsingError(
                "The Auth0 role mappings must be a dict", role_mapping
            )
        return Auth0Authentication(
            issuer, audience, client_id, client_secret, role_mapping
        )

    @classmethod
    def _do_merge(
        cls, instance1: Auth0Authentication, instance2: Auth0Authentication
    ) -> Auth0Authentication:
        """Merge the auth0 authentications."""
        issuer = instance2.issuer if instance2.issuer is not None else instance1.issuer
        audience = (
            instance2.audience if instance2.audience is not None else instance1.audience
        )
        client_id = (
            instance2.client_id
            if instance2.client_id is not None
            else instance1.client_id
        )
        client_secret = (
            instance2.client_secret
            if instance2.client_secret is not None
            else instance1.client_secret
        )
        if instance1.role_mapping is None:
            roles = instance2.role_mapping
        elif instance2.role_mapping is None:
            roles = instance1.role_mapping
        else:
            roles = {**instance1.role_mapping, **instance2.role_mapping}
        return Auth0Authentication(issuer, audience, client_id, client_secret, roles)
