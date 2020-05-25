from datetime import datetime
from typing import List

from pydantic import BaseModel


class CPEInterfaces(BaseModel):
    interface_name: str
    description: str


class CPEVirtualInterface(CPEInterfaces):
    ip: str
    subnetmask: str
    network_type: str
    vrf: str
    ip_helper: List[str]


class CPEPhysicalInterface(CPEInterfaces):
    vlans: List[int]


class CPE(BaseModel):
    hostname: str
    model: str
    circuit_id: str
    bandwidth: int
    virtual_interface: List[CPEVirtualInterface]
    physical_interface: List[CPEPhysicalInterface]
    mgmt_ip: str
    polling_method_snmp: bool
    syslocation: str
    address: str
    zip_code: int
    city: str


class CPEInDB(CPE):
    last_seen: datetime
    first_seen: datetime


class CPEInDBList(BaseModel):
    result: List[CPEInDB]


class CPEDeleted(BaseModel):
    circuit_id: str


class SSHInput(BaseModel):
    username: str
    password: str
    ip: str
    commands: List[str]


class SSHCommandOutput(BaseModel):
    command: str
    output: List[str]


class SSHReturn(BaseModel):
    result: List[SSHCommandOutput]
