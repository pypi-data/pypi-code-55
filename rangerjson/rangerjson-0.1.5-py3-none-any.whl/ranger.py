from dataclasses import dataclass, field
from typing import List,Iterable
from enum import Enum
from functools import reduce
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class Hadoop(Enum):
    knox = "knox"
    yarn = "yarn"
    hdfs = "hdfs"
    hive = "hive"
    hbase = "hbase"
    atlas = "atlas"
    kafka = "kafka"


MAPPING: dict = {
    Hadoop.hdfs: ['path'],
    Hadoop.hive: ['database', 'table'],
    Hadoop.yarn: ['queue'],
    Hadoop.knox: ['topology', 'service'],
    Hadoop.hbase: ['column-family'],
    Hadoop.atlas: ['operation'],
    Hadoop.kafka: ['topic']
}


@dataclass
class Policy:
    data: dict
    service: Hadoop = field(init=False)

    def __post_init__(self):
        self.service = self.guess_service()
        if not self.data:
            raise ValueError("data can not be empty")

    def guess_service(self):
        for k, v in MAPPING.items():
            if any([elt for elt in v if elt in self.data['resources']]):
                return k
        # nothing matched
        raise ValueError("Unable to guess the service")

    def find_access(self, group: str) -> list:
        try:
            return [elt for elt in self.data['policyItems'] if group in elt['groups']][0]['accesses']
        except IndexError:
            return []

    @staticmethod
    def _access2string(acc: list) -> str:
        if not acc:
            return ''
        ok = [elt['type'] for elt in acc if elt['isAllowed']]
        return ', '.join(ok)

    def _short_auth(self, group: str) -> str:
        accesses = self.find_access(group)
        return Policy._access2string(accesses)

    def get_authorization(self, group: str) -> dict:
        """provide authorization & ressource associated

        each element is a dedicated policy in ranger
        """
        authz = self._find_access_str(group)
        if not authz:
            return {}
        return {'authorization': authz, **self.get_ressources()}

    def _find_access_str(self, group) -> str:
        return Policy._access2string(self.find_access(group))

    def get_ressources(self) -> dict:
        return {key: self.data['resources'][key]['values']
                for key in MAPPING[self.service]}

    @staticmethod
    def _flatten(nested:Iterable[List])->List:
        "make a flat list from nested elts"
        if not nested:
            return []
        return reduce(lambda x, y: x+y, nested)

    def get_groups(self) -> list:
        """all groups present in thep policy"""
        return Policy._flatten([elt['groups'] for elt in self.data['policyItems']])


@ dataclass
class Conf:
    data: dict
    group: str
    policies: List[Policy] = field(init=False)
    error: List[dict] = field(init=False)

    def __post_init__(self):
        res = []
        error = []
        for policy in self.data['policies']:
            try:
                policy = Policy(policy)
                if self.group in policy.get_groups():
                    res.append(policy)
            except ValueError as e:
                logger.warning(f'trying to convert to policy error :{e}')
                error.append(policy)
        self.policies = res
        self.error = error

    def get_service(self, service) -> list:
        return [policy for policy in self.policies if policy.service == service]

    def get_autorization(self) -> dict:
        authz = [(policy.service.value, policy.get_authorization(self.group))
                 for policy in self.policies]
        res = defaultdict(list)
        for k, v in authz:
            res[k].append(v)
        return res
