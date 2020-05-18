import logging
import sys

from tracker_master import config as CFG
import tracker_master.util as util
from tracker_master.app_master.configure import MasterConfigure
from tracker_master.app_master.master import TrackerMaster
from tracker_master.app_master.message_queue import MessageQueue
from tracker_master.app_master.notifier import ZabbixNotifier
from tracker_master.app_master.slave_data_consumer import ConfigurerConsumer, SlavesConfigurer
from tracker_master.app_master.slave_data_consumer import MainConsumer
from tracker_master.app_master.slave_data_producer import SlaveReaderThread
from tracker_master.model.app_model import Master
from tracker_master.app_master.missed_data import MissedDataStorage
from tracker_master.app_master.missed_data import MissedDataSender
from tracker_master.zbx_client import ZabbixClient

DEFAULT_PROFILE_NAME = 'development'


def print_conf(_master):
    print_master_conf(_master)
    if _master:
        print_slave_conf(_master.get_slaves())


def print_help():
    print('init master - \tSet master group name and master name for current served object\n'
          'init slaves - \tStart configuring slaves. When slave send signal it registered at the system\n'
          '\t\tPress Enter to stop process\n'
          'init zabbix - \tCreate zabbix configuration for current master at the Zabbix server\n'
          'show config - \tShow current master configuration\n'
          'start \t- \tRun master\n'
          'exit \t- \texit the program\n'
          '? \t- \tshow help\n')


def print_master_conf(_master):
    if _master and isinstance(_master, Master) and _master.is_configured():
        print('## Master: \n# Group: %s\n# Name: %s\n' % (_master.uniq_group_name, _master.uniq_master_name))
    else:
        print('## Master: NOT INITIALIZED\n')


def print_slave_conf(_slaves):
    if _slaves and isinstance(_slaves, dict) and len(_slaves) > 0:
        print('## Slaves: %s slaves configured' % len(_slaves))
        for slave in _slaves.values():
            print('# %s %s' % (slave.zbx_slave_number, slave.hw_id))
        print()
    else:
        print('## Slaves: NOT INITIALIZED\n')


if __name__ == "__main__":
    print_help()
    # Take profile name from args
    profile_name = None
    if len(sys.argv) == 1:
        profile_name = DEFAULT_PROFILE_NAME
    else:
        profile_name = sys.argv[1]
    print('### Profile: %s' % profile_name)

    # Read configure with profile
    CFG.read("../conf/app_master_config.yaml", profile_name)

    # Setup loggin
    util.setup_logging()
    logger = logging.getLogger(__name__)

    tracker_master = TrackerMaster()
    tracker_master.init_from_conf()

    # Main operations
    print_conf(tracker_master.get_master())
    while True:
        cmd = input('Enter command: ')
        if cmd == 'init master':
            print_master_conf(tracker_master.get_master())
            master_group_name = input('Set master group name: ').strip()
            master_name = input('Set master name: ').strip()
            tracker_master.init_master(master_group_name, master_name)
            print_master_conf(tracker_master.get_master())
        elif cmd == 'init slaves':
            print_slave_conf(tracker_master.get_master().get_slaves())
            c = ConfigurerConsumer()
            msg_queue = MessageQueue(SlaveReaderThread(), c)
            msg_queue.start()

            while True:
                cmd = input('Press Enter to finish:\n')
                if cmd == '':
                    msg_queue.stop()
                    tracker_master.init_slaves(c.get_configured_slaves())
                    print_slave_conf(tracker_master.get_master().get_slaves())
                    break
        elif cmd == 'start':
            c = MainConsumer()
            ds = MissedDataStorage(CFG.missed_data_storage_folder())
            zbx_client = ZabbixClient(CFG.zbx_api_url(), CFG.zbx_user(), CFG.zbx_pwd())
            missed_data_sender = MissedDataSender(ds, zbx_client)
            c.add_listener(ZabbixNotifier(tracker_master, ds))
            msg_queue = MessageQueue(SlaveReaderThread(), c)
            msg_queue.start()
            missed_data_sender.start()
            cmd = input('Type \'stop\' to finish:\n')
            if cmd == 'stop':
                msg_queue.stop()
                missed_data_sender.stop_working()

        elif cmd == 'show config':
            print_conf(tracker_master.get_master())
        elif cmd == 'init zabbix':
            zabbix_configure = MasterConfigure(CFG.zbx_api_url(), CFG.zbx_user(), CFG.zbx_pwd())
            zabbix_configure.configure(tracker_master.get_master(), force_create=True)
        elif cmd == 'exit':
            sys.exit()  # todo check resources
        elif cmd == '?':
            print_help()
