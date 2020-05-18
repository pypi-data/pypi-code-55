import logging

from tracker_master.model.app_model import Master
from tracker_master.model.zabbix import ZabbixTrigger
from tracker_master.zbx_client import Fields
from tracker_master.zbx_client import ZabbixClient


class MasterConfigure(ZabbixClient):

    def __init__(self, url, user, password):
        ZabbixClient.__init__(self, url, user, password)
        # Zabbix entities name/id
        self.host_group = None
        self.host_group_id = None
        self.host = None
        self.host_id = None
        self.master_template_id = None
        self.logger = logging.getLogger(MasterConfigure.__name__)

    def configure(self, master, force_create=False, template_name=Fields.ZBX_TEMPLATE_NAME):
        assert isinstance(master, Master)
        slaves = master.get_slaves()
        self.host_group = master.uniq_group_name
        self.host = master.uniq_master_name
        if slaves:
            assert isinstance(slaves, dict)

        self.logger.info('#### Init Zabbix Master configuration ####')
        self.logger.info('## Configure host group \'%s\'' % self.host_group)
        group_id = self.get_host_group_id(self.host_group)
        if group_id is None:
            if force_create:
                group_id = self.create_host_group(self.host_group)
            else:
                self.logger.warning('Host group \'%s\' not exists' % self.host_group)
                return
        if group_id:
            self.host_group_id = group_id
            self.logger.info('## Zabbix host group \'%s\' configured' % self.host_group_id)
        else:
            self.logger.error('Host group creation error')

        self.logger.info('## Looking for template: %s ' % template_name)
        t_id = self.get_template_id(template_name)
        if t_id:
            self.master_template_id = t_id
            self.logger.info('## Zabbix template \'%s\' configured' % self.master_template_id)
        else:
            self.logger.error('Master template is missed')
            return

        self.logger.info('## Configure host \'%s\'' % self.host)
        host_id = self.get_host_id(self.host)
        if host_id is None:
            if force_create:
                host_id = self.create_master_host(self.host, self.host)
            else:
                self.logger.error('Host creation error')
                return
        if host_id:
            self.host_id = host_id
        self.logger.info('## Zabbix host \'%s\' configured' % self.host)

        if not slaves or len(slaves) == 0:
            self.logger.warning('Device list is empty')
            return False
        # Configure devices
        self.logger.info('Find %s devices' % len(slaves))
        slave_items = self.get_host_items(self.host_id)

        active_items_ids = list()
        for slave_idx, slave in slaves.items():
            self.logger.info('Configure %s%s' % (Fields.ZBX_SLAVE_NAME_PREF, slave_idx))
            slave_conf = slave_items[slave_idx]
            slave.monitorings = slave_conf
            for monitoring in slave.monitorings:
                if not monitoring.active:
                    self.enable_item(monitoring)
                    active_items_ids.append(monitoring.id)
                else:
                    active_items_ids.append(monitoring.id)

        triggers = self.get_host_triggers(self.host_id, self.master_template_id)

        for trigger in triggers:
            assert isinstance(trigger, ZabbixTrigger)
            assert len(trigger.items) == 1
            if trigger.items[0] in active_items_ids:
                if not trigger.active:
                    self.enable_trigger(trigger)

        return True