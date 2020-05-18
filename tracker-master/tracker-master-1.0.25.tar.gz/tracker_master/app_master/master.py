import os.path

import yaml

from tracker_master import config as CFG
from tracker_master.model.app_model import Master, Slave


class TrackerMaster:

    def __init__(self):
        self.master = None

    def init(self, master):
        assert isinstance(master, Master)
        self.master = master
        self.__update_conf()

    def init_master(self, master_group_name, master_name):
        self.master = Master(master_group_name, master_name)
        self.__update_conf()

    def init_slaves(self, _dict):
        assert self.master
        self.master.init_slaves(_dict)
        self.__update_conf()

    def is_master_configured(self):
        return self.master and self.master.is_configured()

    def is_slave_configured(self):
        return self.master and self.master.has_slaves()

    def get_master(self) -> Master:
        return self.master

    def __update_conf(self):
        self.__write_conf()
        self.init_from_conf()

    def init_from_conf(self, cfg_path=None):
        if not cfg_path:
            cfg_path = CFG.master_state_configuration()

        if not os.path.exists(cfg_path):
            return False

        with open(cfg_path, 'r') as f:
            cfg = yaml.safe_load(f)
            master = Master(
                cfg.get('master_group'), cfg.get('master_name')
            )
            slaves_cfg_dict = cfg.get('slaves')

            if slaves_cfg_dict:
                slaves_dict = dict()
                for zbx_slave_idx, slave_data in slaves_cfg_dict.items():
                    hw_id = slave_data['hw_id']
                    slave = Slave(hw_id, zbx_slave_idx)
                    slaves_dict[zbx_slave_idx] = slave

                master.set_slaves(slaves_dict)

            self.master = master
            return True

    def __write_conf(self):
        conf = {
            'master_group': self.master.uniq_group_name,
            'master_name': self.master.uniq_master_name
        }

        slaves = self.master.get_slaves()
        slaves_dict = dict()
        if slaves:
            for zbx_slave_idx, slave in slaves.items():
                slaves_dict[zbx_slave_idx] = {
                    'hw_id': slave.hw_id
                }
        conf['slaves'] = slaves_dict
        conf = yaml.dump(conf)

        with open(CFG.master_state_configuration(), 'w') as f:
            f.write(conf)
