import logging
import threading
from socket import timeout

from pyzabbix.sender import ZabbixSender, ZabbixMetric

from tracker_master import config as CFG
from tracker_master.app_master.master import TrackerMaster
from tracker_master.app_master.missed_data import MissedDataStorage
from tracker_master.model.app_model import Message, MonitoringName
from tracker_master.zbx_client import Fields


class MessageListener:

    def receive_message(self, msg_list):
        pass


class ZabbixNotifier(MessageListener):

    def __init__(self, tracker_master, missed_data_storage=None):
        assert isinstance(tracker_master, TrackerMaster)
        self.host_name = tracker_master.get_master().get_uniq_master_name()
        assert isinstance(tracker_master, TrackerMaster)
        self.tracker_master = tracker_master
        self.missed_data_storage = missed_data_storage
        self.logger = logging.getLogger(ZabbixNotifier.__name__)

    def receive_message(self, msg_list):
        zbx_metrics_batch = []
        for msg in msg_list:
            assert isinstance(msg, Message)
            slave = self.tracker_master.get_master().get_slave(msg.hw_id)
            device_name = Fields.ZBX_SLAVE_NAME_PREF + str(slave.zbx_slave_number)
            msg_key_name = device_name + '.' + msg.type.name.lower()
            charge_key_name = device_name + '.' + MonitoringName.CHARGE.value
            zbx_metrics_batch.append(ZabbixMetric(self.host_name, msg_key_name, 1, msg.time))
            zbx_metrics_batch.append(ZabbixMetric(self.host_name, charge_key_name, msg.charge, msg.time))

        sending_thread = ZabbixSenderThread(zbx_metrics_batch, self.missed_data_storage)
        self.logger.debug('Active threads %s' % threading.active_count()) # todo move to separate Thread
        sending_thread.start()


class ZabbixSenderThread(threading.Thread):

    def __init__(self, batch, ds=None):
        threading.Thread.__init__(self)
        assert ds is None or isinstance(ds, MissedDataStorage)
        self.setDaemon(True)
        self.logger = logging.getLogger(ZabbixSenderThread.__name__)
        self.batch = batch
        self.ds = ds
        self.sender = ZabbixSender(CFG.zbx_sender_url())

    def __try_save_missed_data_batch(self):
        if self.ds:
            self.ds.store(self.batch)
        else:
            self.logger.warning('Lost %s messages: %s' % (len(self.batch), self.batch))

    def run(self) -> None:
        try:
            self.logger.debug('Send %s metrics to Zabbix' % len(self.batch))
            resp = self.sender.send(self.batch)
            self.logger.debug('Response: %s' % resp)
            self.__try_save_missed_data_batch() # todo TMP убрать
        except timeout:
            self.logger.error('Lost connection with Zabbix server')
            self.__try_save_missed_data_batch()
        except Exception as ex:
            # todo походу надо разобраться с зависимостями, что бы приходил нормальный эксепшн
            if 'gaierror' in ex.args[0]:
                self.logger.warning('Lost connection with Network')
            else:
                self.logger.error(ex)
            self.__try_save_missed_data_batch()



