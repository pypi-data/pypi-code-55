from dataclasses import dataclass, field
from typing import List
from enum import Enum
from functools import reduce
from collections import defaultdict


class Hadoop(Enum):
    knox = "knox"
    yarn = "yarn"
    hdfs = "hdfs"
    hive = "hive"


MAPPING: dict = {
    Hadoop.hdfs: ['path'],
    Hadoop.hive: ['database', 'table'],
    Hadoop.yarn: ['queue'],
    Hadoop.knox: ['topology', 'service']
}


@dataclass
class Policy:
    data: dict
    service: Hadoop = field(init=False)

    def __post_init__(self):
        self.service = self.guess_service()
        if not self.data:
            raise ValueError("data can not be empty")

    def _is_hdfs(self):
        return 'path' in self.data['resources']

    def _is_yarn(self):
        return 'queue' in self.data['resources']

    def _is_hive(self):
        return 'database' in self.data['resources']

    def _is_knox(self):
        return 'topology' in self.data['resources']

    def guess_service(self):
        if self._is_hdfs():
            return Hadoop.hdfs
        elif self._is_yarn():
            return Hadoop.yarn
        elif self._is_hive():
            return Hadoop.hive
        elif self._is_knox():
            return Hadoop.knox
        else:
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

    def get_groups(self) -> list:
        """all groups present in thep policy"""
        def flatten(nested):
            return reduce(lambda x, y: x+y, nested)
        return flatten([elt['groups'] for elt in self.data['policyItems']])


@ dataclass
class Conf:
    data: dict
    group: str
    policies: List[Policy] = field(init=False)

    def __post_init__(self):
        policies = [Policy(policy) for policy in self.data['policies']]
        # filter out what is not relevant for my group
        self.policies = [
            policy for policy in policies if self.group in policy.get_groups()]

    def get_service(self, service) -> list:
        return [policy for policy in self.policies if policy.service == service]

    def get_autorization(self) -> dict:
        authz = [(policy.service.value, policy.get_authorization(self.group))
                 for policy in self.policies]
        res = defaultdict(list)
        for k, v in authz:
            res[k].append(v)
        return res

        # return [{policy.service: policy.get_authorization(self.group) for policy in self.policies}]
