import logging
import os
import json
import time
import threading
from socket import timeout

from pyzabbix.sender import ZabbixSender, ZabbixMetric
from pyzabbix.sender import ZabbixMetric

from tracker_master import config as CFG
from tracker_master import util
from tracker_master.zbx_client import ZabbixClient


MAX_RETRY_CNT = 3
TMP_DATA_FILE_SUFFIX = '_'


class MissedDataStorage:

    def __init__(self, storage_dir):
        self.logger = logging.getLogger(MissedDataStorage.__name__)
        self.storage_dir = storage_dir

        # Oldest file with missed messages. Init in __update_state()
        self.current_file = None
        # list of storage_dir data files names. Init in __update_state()
        self.data_files = None
        self.__remove_not_finished_files()
        self.update_state()

    'message_batch - batch of model.Message objects'
    def store(self, message_batch, file=None):
        if file is None:
            if self.current_file is None:
                self.current_file = self.__get_current_period_file_name()
            file = self.__full_name(self.current_file)

        self.logger.info('Store %s messages to missed data log %s' % (len(message_batch), file))
        with open(file, 'a+') as f:
            # ZabbixMetrix.__repr__ has json view
            f.writelines(repr(message_batch))
            f.write('\n')

    def get_current_data_file(self) -> str:
        if self.current_file:
            current_period_file = self.__get_current_period_file_name()
            if self.current_file != current_period_file:
                return self.__full_name(current_period_file)
            else:
                return self.__full_name(self.current_file)
        else:
            return None

    def get_oldest_data_file(self) -> str:
        if len(self.data_files) > 1:
            # Файлов несколько. Отдаем самый старший
            return self.__full_name(self.data_files[-1])
        elif len(self.data_files) == 1 and self.get_current_data_file() is None:
            # Файл один и он не текущий (т.е. никто в него уже не будет писать)
            return self.__full_name(self.data_files[0])

        return None

    def __full_name(self, file_name):
        return self.storage_dir + os.altsep + file_name

    def __remove_not_finished_files(self):
        files = os.listdir(self.storage_dir)
        for file in files:
            if file.endswith(TMP_DATA_FILE_SUFFIX):
                self.logger.info('File %s was not processed completely. Remove it' % file)

    def update_state(self):
        files = os.listdir(self.storage_dir)
        if files and len(files) > 0:
            logging.warning('There are missed data files: %s' % files)
            files = [f.strip('\'') for f in files]
            files.sort()

            self.data_files = files
            current_period_file = self.__get_current_period_file_name()
            if files[0] == current_period_file:
                self.current_file = current_period_file
        else:
            self.current_file = None
            self.data_files = list()
            return

    def __get_current_period_file_name(self):
        return util.format_current_time('%Y_%b_%d_%H.%M.json')


class MissedDataSender(threading.Thread):

    def __init__(self, ds, zbx_client):
        super(MissedDataSender, self).__init__()
        assert isinstance(ds, MissedDataStorage)
        self.logger = logging.getLogger(MissedDataSender.__name__)
        self.ds = ds
        assert isinstance(zbx_client, ZabbixClient)
        self.zbx_client = zbx_client
        self.is_running = True
        self.setDaemon(True)

    def run(self) -> None:
        while True:
            self.do_work()
            time.sleep(5)  # todo move to config

    def do_work(self):
        while True and self.is_running:
            df = self.ds.get_oldest_data_file()
            if not df:
                current_data_file = self.ds.get_current_data_file()
                if current_data_file is None:
                    self.logger.info('There are no missed messages')
                else:
                    self.logger.info('There are %s with missed messages. It will be processed later' % current_data_file)
                return

            self.logger.info('Try resend data from %s' % df)
            batches = list()
            with open(df, 'r') as f:
                while True:
                    msgs_str = f.readline()
                    if not msgs_str:
                        break

                    try:
                        metrics = self.__parse_metrics_batch(msgs_str)
                        batches.append(metrics)
                    except Exception as ex:
                        self.logger.warning('Exception on parsing missed data batch: %s' % msgs_str)


            # todo Optimize. Compact batches

            is_no_failed_data = True
            tmp_data_file = df + TMP_DATA_FILE_SUFFIX
            for batch in batches:
                if self.send(batch):
                    self.logger.info('Successfully sent %s missed messages' % len(batch))
                    continue
                else:
                    self.ds.store(batch, tmp_data_file)
                    is_no_failed_data = False

            if is_no_failed_data:
                os.remove(df)
            elif os.path.exists(tmp_data_file):
                os.remove(df)
                self.logger.debug('Rename %s to %s' % (tmp_data_file, df))
                os.rename(tmp_data_file, df)

            self.ds.update_state()

    def stop_working(self):
        self.is_running = False

    def send(self, batch):
        if not self.zbx_client.ping():
            return False
        zabbix_sender = ZabbixSenderThread(batch, self.ds)
        zabbix_sender.start()
        zabbix_sender.join()
        return not zabbix_sender.failed

    def __parse_metrics_batch(self, msgs_str) -> list:
        metrics = list()
        for dict_data in json.loads(msgs_str):
            assert isinstance(dict_data, dict)
            # todo move that logic to another place
            metrics.append(ZabbixMetric(dict_data['host'], dict_data['key'], dict_data['value'], dict_data['clock']))
        return metrics


# todo В Notifier есть почти такой-же класс. Избавиться от дублирования.
class ZabbixSenderThread(threading.Thread):

    def __init__(self, batch, ds=None):
        threading.Thread.__init__(self)
        assert ds is None or isinstance(ds, MissedDataStorage)
        self.logger = logging.getLogger(ZabbixSenderThread.__name__)
        self.batch = batch
        self.ds = ds
        self.failed = False
        self.sender = ZabbixSender(CFG.zbx_sender_url())

    def __try_save_missed_data_batch(self):
        self.failed = True
        if self.ds:
            self.ds.store(self.batch)
        else:
            self.logger.warning('Lost %s messages: %s' % (len(self.batch), self.batch))

    def run(self) -> None:
        try:
            self.logger.debug('Send %s metrics to Zabbix' % len(self.batch))
            resp = self.sender.send(self.batch)
            self.logger.debug('Response: %s' % resp)
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