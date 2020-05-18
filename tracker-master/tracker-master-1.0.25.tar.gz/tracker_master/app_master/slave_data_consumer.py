import logging

from tracker_master.app_master.message_queue import MessageQueueWorker
from tracker_master.app_master.notifier import MessageListener
from tracker_master.model.app_model import Slave


class MainConsumer(MessageQueueWorker):

    def __init__(self):
        # todo move sleep duration settings
        super(MainConsumer, self).__init__(sleep_duration=2)
        self.listeners = list()
        self.logger = logging.getLogger(MainConsumer.__name__)
        self.batch = list()

    def do_work(self):
        if not self.is_empty_queue():
            while not self.is_empty_queue():
                self.batch.append(self.get_next_message())
            self.logger.debug('Batch size: %s' % len(self.batch))

        if len(self.batch) != 0:
            for listener in self.listeners:
                self.logger.debug("Receive %s messages" % len(self.batch))
                try:
                    listener.receive_message(self.batch)
                except Exception as ex:
                    self.logger.error(ex)

            self.batch = list()
        return True

    def add_listener(self, listener):
        assert isinstance(listener, MessageListener)
        self.listeners.append(listener)


class ConfigurerConsumer(MessageQueueWorker):

    def __init__(self):
        super(ConfigurerConsumer, self).__init__()
        self.logger = logging.getLogger(ConfigurerConsumer.__name__)
        self.slave_configurer = SlavesConfigurer()
        return

    def do_work(self):
        if not self.is_empty_queue():
            msg = self.get_next_message()
            self.logger.debug('Recieved message: %s' % msg)
            self.slave_configurer.register_slave(msg)
            return True

    def get_configured_slaves(self):
        return self.slave_configurer.slaves


class SlavesConfigurer:

    def __init__(self):
        self.slaves = dict()
        self.logger = logging.getLogger(SlavesConfigurer.__name__)

    def register_slave(self, msg):
        slave = Slave(msg.hw_id)
        if slave in self.slaves.values():
            self.logger.info('Slave %s is already existed' % msg.hw_id)
            return False

        zbx_new_slave_idx = len(self.slaves) + 1
        slave.zbx_slave_number = zbx_new_slave_idx
        self.slaves[zbx_new_slave_idx] = slave
        self.logger.info('Slave %s %s has registered' % (zbx_new_slave_idx, msg.hw_id))
        return True



