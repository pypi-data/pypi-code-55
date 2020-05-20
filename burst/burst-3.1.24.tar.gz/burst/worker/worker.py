
import signal
import setproctitle
import os

from .connection import Connection
from ..share.log import logger
from .request import Request
from ..share import constants


class Worker(object):

    type = constants.PROC_TYPE_WORKER

    request_class = Request
    connection_class = Connection
    got_first_request = False

    group_id = None

    # 是否有效(父进程中代表程序有效，子进程中代表worker是否有效)
    enabled = True
    # 是否已经发送KeyboardInterrupt
    got_keyboard_interrupt = False

    def __init__(self, app, group_id):
        """
        构造函数
        :return:
        """
        self.app = app
        self.group_id = group_id

    def run(self):
        setproctitle.setproctitle(self.app.make_proc_name(
            '%s:%s' % (self.type, self.group_id)
        ))

        self._handle_proc_signals()
        self._on_start()

        try:
            address = os.path.join(
                self.app.config['IPC_ADDRESS_DIRECTORY'],
                self.app.config['WORKER_ADDRESS_TPL'] % self.group_id
            )
            conn = self.connection_class(self, address, self.app.config['WORKER_CONN_TIMEOUT'])
            conn.run()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur. worker: %s', self, exc_info=True)
        finally:
            self._on_stop()

    def _on_start(self):
        self.app.events.start_worker(self)
        for bp in self.app.blueprints:
            bp.events.start_app_worker(self)

    def _on_stop(self):
        for bp in self.app.blueprints:
            bp.events.stop_app_worker(self)
        self.app.events.stop_worker(self)

    def _handle_proc_signals(self):
        def stop_handler(signum, frame):
            self.enabled = False
            # 防止重复发送KeyboardInterrupt
            # 因为在终端直接CTRL-C是会自动往子进程发送的
            # 但是kill -INT不会
            if not self.got_keyboard_interrupt:
                self.got_keyboard_interrupt = True
                raise KeyboardInterrupt

        def safe_stop_handler(signum, frame):
            self.enabled = False

        # 强制结束，抛出异常终止程序进行
        signal.signal(signal.SIGINT, stop_handler)
        # 安全停止
        signal.signal(signal.SIGTERM, safe_stop_handler)
        signal.signal(signal.SIGHUP, safe_stop_handler)

    def __repr__(self):
        return '<%s name: %s, group_id: %r>' % (
            type(self).__name__, self.app.name, self.group_id
        )
