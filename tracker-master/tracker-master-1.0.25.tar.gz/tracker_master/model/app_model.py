from enum import Enum


class MessageType(Enum):
    ALARM = 1
    TEST = 2
    PING = 3


class MonitoringName(Enum):
    ALARM = 'alarm'
    CHARGE = 'charge'
    TEST = 'test'


class Master:

    def __init__(self, uniq_group_name, uniq_master_name):
        self.uniq_group_name = uniq_group_name
        self.uniq_master_name = uniq_master_name
        # zabbix_slave_number -> Slave
        self.slaves = dict()
        # hardware id -> Slave
        self.hw_id_to_slaves = dict()

    def set_slaves(self, slaves):
        assert isinstance(slaves, dict)
        self.slaves = slaves
        for slave in self.slaves.values():
            assert isinstance(slave, Slave)
            self.hw_id_to_slaves[slave.hw_id] = slave

    def get_slave(self, hw_id):
        return self.hw_id_to_slaves[hw_id]

    def get_slaves(self):
        return self.slaves

    def is_configured(self) -> bool:
        return self.uniq_group_name and self.uniq_master_name

    def has_slaves(self) -> bool:
        return self.slaves and len(self.slaves) > 0

    def get_uniq_group_name(self):
        return self.uniq_group_name

    def get_uniq_master_name(self):
        return self.uniq_master_name


class Message:

    def __init__(self, hw_id, _type, charge, _time=None, retry_cnt=0):
        # slave hardware id
        self.hw_id = hw_id
        # MessageType
        self.type = MessageType(_type)
        # Amount of slave charge
        self.charge = charge
        # Unix timestamp
        self.time = _time
        self.retry_count = retry_cnt

    def __str__(self):
        return "%s %s %s %s %s" % (self.hw_id, self.type.name, self.charge, self.time or 0, self.retry_count)


class Slave:

    def __init__(self, hw_id, zbx_slave_number=0):
        self.hw_id = hw_id
        self.zbx_slave_number = zbx_slave_number

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Slave) and self.hw_id == o.hw_id

    def __hash__(self) -> int:
        return hash(self.hw_id)