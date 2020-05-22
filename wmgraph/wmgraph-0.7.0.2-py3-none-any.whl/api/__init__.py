import json
import logging

from ..utils import jdump

from .base import MgraphBase
from .drive import MgraphConnectorDriveMixin
from .group import MgraphConnectorGroupMixin
from .usercontact import MgraphConnectorUserContactMixin
from .site import MgraphConnectoSiteMixin
from .user import MgraphConnectorUserMixin
from .deleted import MgraphConnectorDeletedMixin
from .auditlogs import MgraphConnectorAuditlogsMixin

class MgraphApi(
        MgraphBase,
        MgraphConnectorDriveMixin,
        MgraphConnectorGroupMixin,
        MgraphConnectorUserMixin,
        MgraphConnectoSiteMixin,
        MgraphConnectorUserContactMixin,
        MgraphConnectorAuditlogsMixin,
        MgraphConnectorDeletedMixin,
        ):
    pass
