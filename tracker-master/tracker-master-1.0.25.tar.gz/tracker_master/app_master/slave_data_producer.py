import logging

import serial

from tracker_master import util, config as CFG
from tracker_master.app_master.message_queue import MessageQueueWorker
from tracker_master.model.app_model import Message


def parse(message_string) -> Message:
    return Message(hw_id=int(message_string[0:8]),
                   _type=int(message_string[8]),
                   charge=float(message_string[9:13]))


class SlaveReaderThread(MessageQueueWorker):

    def __init__(self):
        super(SlaveReaderThread, self).__init__()
        self.port_logger = util.get_com_port_logger()
        self.logger = logging.getLogger(SlaveReaderThread.__name__)
        self.setDaemon(True)

    def run(self):

            ''' If a timeout is set it may
                    return less characters as requested. With no timeout it will block
                    until the requested number of bytes is read. '''
            with serial.Serial(CFG.slave_com_port(), CFG.slave_com_port_baudrate()) as ser:
                while self.is_running:
                    try:
                        msg = ser.readline().decode().strip()
                        self.port_logger.info(msg)
                        message = parse(msg)
                        message.time = util.unix_time()
                        self.put_message(message)
                    except Exception as ex:
                        self.logger.error('Parse message error:' + ex)
