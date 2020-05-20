from typing import Union, List

from httpx import Client as HTTPXClient
from httpx import AsyncClient as HTTPXAsyncClient
from netauto._exceptions import RegexAndNoneRegexParm

from ._validate import validate_200, validate_201

from netauto.models.cpe import CPEInDBList, CPEInDB, CPEDeleted, SSHInput, SSHReturn
from netauto.models.cpe import CPE as CPEModel


class BaseCPE:

    def __init__(self, session: Union[HTTPXClient, HTTPXAsyncClient]):
        self._session = session
        self._base_url = "cpe/"

    @staticmethod
    def _regex_params(params: dict,
                      regex_circuit_id: Union[None, str],
                      regex_mgmt_ip: Union[None, str],
                      regex_address: Union[None, str]) -> dict:

        if regex_circuit_id:
            if params["circuit_id"]:
                raise RegexAndNoneRegexParm("it is not allowed to have both regex and none regex")
            else:
                params["circuit_id"] = f"~{regex_circuit_id}"
        if regex_mgmt_ip:
            if params["mgmt_ip"]:
                raise RegexAndNoneRegexParm("it is not allowed to have both regex and none regex")
            else:
                params["mgmt_ip"] = f"~{regex_mgmt_ip}"
        if regex_address:
            if params["address"]:
                raise RegexAndNoneRegexParm("it is not allowed to have both regex and none regex")
            else:
                params["address"] = f"~{regex_address}"

        for k, v in params.copy().items():
            if v is None:
                del params[k]

        return params


class CPE(BaseCPE):

    def __init__(self, session: HTTPXClient):
        super().__init__(session=session)

    def get_cpe(self,
                circuit_id: str = None,
                bandwidth: int = None,
                mgmt_ip: str = None,
                polling_method_snmp: bool = None,
                address: str = None,
                zip_code: int = None,
                regex_circuit_id: str = None,
                regex_mgmt_ip: str = None,
                regex_address: str = None,
                limit: int = 10) -> CPEInDBList:
        params = dict(circuit_id=circuit_id,
                      bandwidth=bandwidth,
                      mgmt_ip=mgmt_ip,
                      polling_method_snmp=polling_method_snmp,
                      address=address,
                      zip_code=zip_code,
                      limit=limit)
        params = self._regex_params(params=params,
                                    regex_circuit_id=regex_circuit_id,
                                    regex_mgmt_ip=regex_mgmt_ip,
                                    regex_address=regex_address)
        r = self._session.get(url=self._base_url, params=params)
        validate_200(r=r)
        return CPEInDBList(**r.json())

    def create_cpe(self, cpe: CPEModel) -> CPEInDB:
        r = self._session.post(url=self._base_url, json=cpe.dict())
        validate_201(r=r)
        return CPEInDB(**r.json())

    def delete_cpe(self, circuit_id: str):
        params = dict(circuit_id=circuit_id)
        r = self._session.delete(url=self._base_url, params=params)
        validate_200(r=r)
        return CPEDeleted(**r.json())

    def ssh(self, username: str, password: str, ip: str, commands: List[str]) -> SSHReturn:
        input_data = SSHInput(username=username, password=password, ip=ip, commands=commands)
        r = self._session.post(url=f"{self._base_url}ssh/", json=input_data.dict(), timeout=20)
        validate_201(r=r)
        return SSHReturn(**r.json())
