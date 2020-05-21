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

class MgraphApiMockX(MgraphApi):
    def __init__(self, params='config.json', database=None, args=None): # pylint: disable=super-init-not-called
        self.database = database
        self.args = args

class MgraphApiMock(MgraphApi):
    def get(self, url, params=None, cache_id=None):
        '''cache and mock'''
        item_id = f"{url}?{params}"
        res = self.database.requests.find_one(item_id=item_id)
        if res:
            res = json.loads(res['data'])
            if self.args.v:
                jdump(res, caller=__file__)
            logging.debug(f'cached response {item_id}')
        else:
            res = super(MgraphApiMock, self).get(url, params=params)
            self.database.requests.insert(dict(item_id=item_id, data=json.dumps(res)))
            logging.debug(f'cached request {item_id}')
        return res
