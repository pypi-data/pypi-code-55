import logging
import time

from pyzabbix.api import ZabbixAPI

from tracker_master.model.zabbix import HistoryItem, ZabbixItem, ZabbixTrigger
from tracker_master.model.app_model import MonitoringName

logger = logging.getLogger(__name__)


class Fields:
    JSON_API_ENTITY_HOST = 'host'
    JSON_API_ENTITY_TEMPLATE = 'template'
    JSON_API_ENTITY_HOST_GROUP = 'hostgroup'

    ## Zabbix json API fields
    JSON_RESP_ = 'result'
    JSON_RESP_ITEM_ID = 'itemid'
    JSON_RESP_GROUP_ID = 'groupid'
    JSON_RESP_GROUP_IDS = 'groupids'
    JSON_RESP_HOST_ID = 'hostid'
    JSON_RESP_HOST_IDS = 'hostids'
    JSON_RESP_TEMPLATE_IDS = 'templateids'
    JSON_RESP_TEMPLATE_ID = 'templateid'

    JSON_RESP_NAME = 'name'
    JSON_RESP_KEY = 'key_'
    JSON_RESP_STATUS = 'status'

    ZBX_ITEM_TYPE_TRAPPER = 2  # Zabbix Trapper

    ## Zabbix application entities
    ZBX_SLAVE_NAME_PREF = 'Slave_'
    ZBX_TEMPLATE_GROUP_NAME = 'TrackerMaster Template group'
    ZBX_TEMPLATE_NAME = 'TrackerMaster template'

    ## Zabbix test application entities
    ZBX_TEST_TEMPLATE_GROUP_NAME = 'IntegrationTest Template group'
    ZBX_TEST_TEMPLATE_NAME = 'IntegrationTest template'


class ZabbixClient:
    web_api = None

    def __init__(self, url, user, password):
        self.logger = logging.getLogger(ZabbixClient.__name__)
        # ZabbixApi client try connect to server on object constructon
        self.logger.info('Connect to %s as %s' % (url, user))
        while True:
            try:
                self.web_api = ZabbixAPI(url=url, user=user, password=password)
                break
            except Exception:
                self.logger.warning('Can not connect with Zabbix server. Try to reconnect')
                time.sleep(5)

    def get_host_group_id(self, name):
        logger.info('Request host group by name %s' % name)
        response = self.web_api.do_request('hostgroup.get', {'filter': {'name': name}})

        host_list = response[Fields.JSON_RESP_]
        host_cnt = len(host_list)
        logger.info('Find %s host groups' % host_cnt)
        if host_cnt == 1:
            logger.info('Host group % already exists' % name)
            return host_list[0][Fields.JSON_RESP_GROUP_ID]

        return None

    def get_host_id(self, name):
        logger.info('Request host by name %s' % name)
        response = self.web_api.do_request('host.get', {'filter': {'host': [name]}})
        host_list = response[Fields.JSON_RESP_]
        host_cnt = len(host_list)
        logger.info('Find %s hosts' % host_cnt)
        if host_cnt == 1:
            return host_list[0][Fields.JSON_RESP_HOST_ID]
        elif host_cnt == 0:
            logger.warning("Host %s does not exists" % name)
        else:
            logger.warning("There are too many hosts with %s name" % name)

        return None

    def delete_host_group(self, template_id) -> bool:
        return self.__delete_zabbix_entity(Fields.JSON_API_ENTITY_HOST_GROUP, template_id, Fields.JSON_RESP_GROUP_IDS)

    def delete_template(self, template_id) -> bool:
        return self.__delete_zabbix_entity(Fields.JSON_API_ENTITY_TEMPLATE, template_id, Fields.JSON_RESP_TEMPLATE_IDS)

    def delete_host(self, host_id) -> bool:
        return self.__delete_zabbix_entity(Fields.JSON_API_ENTITY_HOST, host_id, Fields.JSON_RESP_HOST_IDS)

    def get_group_hosts(self, group_id) -> list:
        logger.info('Request host by group id %s' % group_id)
        response = self.web_api.do_request('host.get', {'filter': {'groupids': [group_id]}})
        host_list = response[Fields.JSON_RESP_]
        host_ids = self.__values_from_list_dict(host_list, 'hostid')
        host_cnt = len(host_ids)
        logger.debug('Find %s hosts' % host_cnt)
        return host_list

    def get_template_id(self, template_name, group_id=None):
        logger.info('Request template by name %s' % template_name)
        params_dict = {'filter': {'host': template_name}}
        if group_id:
            params_dict['groupids'] = [group_id]
        response = self.web_api.do_request('template.get', {'filter': {'host': template_name}})
        host_list = response[Fields.JSON_RESP_]
        host_cnt = len(host_list)
        logger.info('Find %s templates' % host_cnt)
        if host_cnt == 1:
            logger.info('Template %s exists' % template_name)
            return host_list[0][Fields.JSON_RESP_TEMPLATE_ID]

        return None

    def get_template_items(self, template_id) -> dict:
        logger.info('Request template items for %s' % template_id)
        response = self.web_api.do_request('item.get', {Fields.JSON_RESP_TEMPLATE_IDS: [template_id]})
        items = self.__map_template_items(response[Fields.JSON_RESP_])
        logger.info('Find %s template items' % len(items))
        return items

    def get_host_items(self, host_id, active_only=False) -> dict:
        response = self.web_api.do_request('item.get',
                                           {'hostids': host_id, 'sortfield': "name"})
        host_items_j = response[Fields.JSON_RESP_]
        assert isinstance(host_items_j, list)
        items = self.__map_template_items(host_items_j, active_only)
        logger.info('Find %s host items' % len(items))
        return items

    '''
    type: data_type: type: int
        0 - numeric float
        1 - character
        2 - log
        3 - numeric unsigned; (default)
        4 - text
    '''
    def get_history(self, host_ids, data_type=3, time_from=None, time_till=None):
        logger.info('Request history data')
        params_dict = {'history': data_type}
        if time_from:
            params_dict['time_from'] = time_from
        if time_till:
            params_dict['time_till'] = time_till
        if host_ids:
            params_dict['hostids'] = host_ids

        response = self.web_api.do_request('history.get', params_dict)
        history_list = response[Fields.JSON_RESP_]

        result_list = list()
        for item in history_list:
            result_list.append(HistoryItem(int(item['itemid']), int(item['clock']), str(item['value'])))
        return result_list

    def create_group_if_not_exists(self, group_name):
        group_id = self.get_host_group_id(group_name)
        if group_id is None:
            group_id = self.create_host_group(group_name)

        if group_id is None:
            # todo Critical
            logger.critical('Host group %s not initialized' % group_name)
            return False

        logger.info('Host group %s configured' % group_name)
        return group_id

    def create_host_group(self, name):
        logger.info('Create host group %s' % name)
        response = self.web_api.do_request('hostgroup.create', {'name': name})
        group_id = int(response[Fields.JSON_RESP_][Fields.JSON_RESP_GROUP_IDS][int(0)])  # todo check if errors
        return group_id

    def get_host_triggers(self, host_id, template_id) -> list:
        response = self.web_api.do_request('trigger.get',
                                           {'hostids': host_id, 'selectItems': '', 'templateids': template_id})
        trigger_items_j = response[Fields.JSON_RESP_]
        assert isinstance(trigger_items_j, list)

        triggers = list()
        for trigger_j in trigger_items_j:
            id = str(trigger_j['triggerid'])
            is_monitoring_active = int(trigger_j['status']) == 0
            trigger = ZabbixTrigger(id, is_monitoring_active)
            items = trigger_j['items']
            for item in items:
                trigger.items.append(item['itemid'])
            triggers.append(trigger)

        return triggers

    def create_host_if_not_exists(self, host_name):  # todo duplicated with __create_group_if_not_exists
        # todo Try to find Zabbix host group with name served_object_id
        host_id = self.get_host_id(host_name)
        if host_id is None:
            host_id = self.create_master_host(host_name)

        if host_id is None:
            # todo Critical
            self.logger.critical('Host \'%s\' not initialized' % host_name)
            return False

        self.logger.info('Host \'%s\' configured' % host_name)
        return host_id

    def create_master_host(self, name, view_name):
        response = self.web_api.do_request('host.create', {
            'host': name,
            'name': view_name,
            'interfaces': [
                {
                    'type': 1,
                    'main': 1,
                    'useip': 1,
                    'ip': '127.0.0.1',
                    'dns': '',
                    'port': '10050'
                }
            ],
            'templates': [
                {
                    'templateid': self.master_template_id
                }
            ],
            'groups': [{'groupid': self.host_group_id}]

        })
        host_id = int(response[Fields.JSON_RESP_][Fields.JSON_RESP_HOST_IDS][int(0)])  # todo check if errors
        return host_id

    def enable_item(self, item):
        response = self.web_api.do_request('item.update', {'hostids': self.host_id, 'itemid': item.id,
                                                           'status': 0})  # todo create status mapping or const
        host_items_j = response[Fields.JSON_RESP_]

    def enable_trigger(self, trigger):
        response = self.web_api.do_request('trigger.update', {'hostids': self.host_id, 'triggerid': trigger.id,
                                                              'status': 0})  # todo create status mapping or const
        host_items_j = response[Fields.JSON_RESP_]

    def ping(self) -> bool:
        # todo now just check service template which have to be created before any work
        return self.get_template_id(Fields.ZBX_TEST_TEMPLATE_NAME) is not None
        #return self.get_template_id(Fields.ZBX_TEMPLATE_NAME) is not None

    def __delete_zabbix_entity(self, entity_name, entity_id, id_field) -> bool:
        logger.info('Remove %s by id %s' % (entity_name, entity_id))
        # do host.delete, template.delete etc
        response = self.web_api.do_request('%s.delete' % entity_name, [entity_id])
        entity_ids = response[Fields.JSON_RESP_][id_field]
        entity_cnt = len(entity_ids)
        if entity_cnt == 1:
            logger.info('%s with %s has been removed' % (entity_name, entity_id))
            return True
        elif entity_cnt == 0:
            logger.warning("%s %s does not exists" % (entity_name, entity_id))

        return False

    def __values_from_list_dict(self, list_dict, key_name):
        assert isinstance(list_dict, list)
        resp = list()
        for v in list_dict:
            resp.append(v[key_name])
        return resp

    def __map_template_items(self, json_items, active_only=False) -> dict:
        slave_items = dict()
        for item_j in json_items:
            key_name = str(item_j['key_'])
            if not key_name.startswith(Fields.ZBX_SLAVE_NAME_PREF):
                continue

            slave_info = key_name.split('.')
            slave_name = slave_info[0]
            slave_number = int(slave_name[len(Fields.ZBX_SLAVE_NAME_PREF):])
            slave_monitoring = slave_info[1]  # todo check monitoring name in MonitoringName
            is_monitoring_active = int(item_j['status']) == 0
            if active_only and not is_monitoring_active:
                continue
            monitoring_id = item_j['itemid']
            monitoring = ZabbixItem(monitoring_id, MonitoringName(slave_monitoring), is_monitoring_active)
            if slave_number not in slave_items:
                items_list = slave_items[slave_number] = list()
            items_list.append(monitoring)

        return slave_items
