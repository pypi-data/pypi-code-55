import logging

from tracker_master.model.app_model import MonitoringName
from tracker_master.zbx_client import Fields
from tracker_master.zbx_client import ZabbixClient

module_logger = logging.getLogger(__name__)

MASTER_DEVICE_MAX_CNT = 100

devices_conf = [{'key': MonitoringName.CHARGE.value, 'value_type': 0, 'delay': 10},  # todo think about delay
                {'key': MonitoringName.ALARM.value, 'value_type': 3, 'delay': 10},  #
                {'key': MonitoringName.TEST.value, 'value_type': 3, 'delay': 10}]


class ServerConfigurer(ZabbixClient):

    def __init__(self, url, user, password, config):
        ZabbixClient.__init__(self, url=url, user=user, password=password)
        assert isinstance(config, ZabbixServerConfiguration)
        self.logger = logging.getLogger(ServerConfigurer.__name__)
        self.config = config

    # todo Move to other program used by admin
    def configure(self):
        self.logger.info('#### Init Zabbix Server configuration ####')

        # Initialize template group (create if not exists)
        self.logger.info('Check template group \'%s\' exists' % self.config.tg_name)

        tg_id = self.get_host_group_id(self.config.tg_name)
        if tg_id is None:
            tg_id = self.create_host_group(self.config.tg_name)

        if tg_id is None:
            # todo Critical
            self.logger.error('Host group \'%s\' not initialized' % self.config.tg_name)
            return False

        self.logger.info('Host group \'%s\' has been configured' % self.config.tg_name)

        # Initialize template (create if not exists)
        self.logger.info('Check template %s exists' % self.config.t_name)
        tmpl_id = self.get_template_id(self.config.t_name)
        if not tmpl_id:
            response = self.web_api.do_request('template.create', {
                'host': self.config.t_name,
                'groups': {Fields.JSON_RESP_GROUP_ID: tg_id}
            })
            tmpl_id = response[Fields.JSON_RESP_][Fields.JSON_RESP_TEMPLATE_IDS][0]  # Todo check exists

        if tmpl_id is None:
            # todo Critical
            self.logger.error('Template %s not initialized' % self.config.t_name)
            return False

        self.logger.info('Template %s configured' % self.config.t_name)

        # Initialize template items
        self.logger.info('Check template items')
        response = self.web_api.do_request('item.get', {'hostids': tmpl_id, 'sortfield': "name"})
        items_list = response[Fields.JSON_RESP_]
        if len(items_list) == 0:
            self.logger.info('Create template items')
            for zbx_device_idx in range(1, self.config.device_cnt + 1):
                for conf in devices_conf:
                    slave_name = '%s%s' % (self.config.slv_pre_name, zbx_device_idx)
                    self.create_slave_item('%s.%s' % (slave_name, conf['key']),
                                           '%s.%s' % (slave_name, conf['key']),
                                           tmpl_id, Fields.ZBX_ITEM_TYPE_TRAPPER,
                                           conf['value_type'], conf['delay'])

                self.create_trigger(zbx_device_idx, slave_name, MonitoringName.ALARM, 'last()', '=1')
                self.create_trigger(zbx_device_idx, slave_name, MonitoringName.CHARGE, 'last()', '<=1')

        elif len(items_list) == len(devices_conf) * MASTER_DEVICE_MAX_CNT:
            self.logger.info('Template items already created')
        else:
            self.logger.warning('Template has %s items but %s expected.')  # todo write guide message for manual check

        self.logger.info('Server configured')

    # parent_id - host_id or template_id
    def create_slave_item(self, name, key, parent_id, type, value_type, delay_sec):
        message = {'name': name,
                   'key_': key,
                   'hostid': str(parent_id),
                   'type': type,
                   'value_type': value_type,
                   'delay': delay_sec,
                   'status': 1
                   }
        self.logger.info('Create item: %s' % message)
        response = self.web_api.do_request('item.create', message)

    def create_trigger(self, zbx_device_idx, slave_name, mon_name, func, expr):
        assert isinstance(mon_name, MonitoringName)
        template_name = self.config.t_name
        monitoring_name = '%s%s.%s' % (self.config.slv_pre_name, zbx_device_idx, mon_name.name.lower())
        expression = '{%s:%s.%s}%s' % (template_name, monitoring_name, func, expr)
        message = {'description': '%s' % slave_name,
                   'expression': expression,
                   'priority': '4',  # high priority
                   'status': 1  # disabled
                   }
        self.logger.info('Create trigger: %s' % message)
        response = self.web_api.do_request('trigger.create', message)


class ZabbixServerConfiguration:

    def __init__(self, tg_name, t_name, slv_pre_name, device_cnt):
        # Service Template group name
        self.tg_name = tg_name
        # Service Template name
        self.t_name = t_name
        # Slave name prefix
        self.slv_pre_name = slv_pre_name
        # Maximum device count
        self.device_cnt = device_cnt


# todo make refactor
class ProductionConfiguration(ZabbixServerConfiguration):

    def __init__(self):
        ZabbixServerConfiguration.__init__(self,
                                           Fields.ZBX_TEMPLATE_GROUP_NAME,
                                           Fields.ZBX_TEMPLATE_NAME,
                                           Fields.ZBX_SLAVE_NAME_PREF,
                                           10)


# todo make singleton?
class IntegrationTestConfiguration(ZabbixServerConfiguration):

    def __init__(self):
        ZabbixServerConfiguration.__init__(self,
                                           Fields.ZBX_TEST_TEMPLATE_GROUP_NAME,
                                           Fields.ZBX_TEST_TEMPLATE_NAME,
                                           Fields.ZBX_SLAVE_NAME_PREF,
                                           5)
