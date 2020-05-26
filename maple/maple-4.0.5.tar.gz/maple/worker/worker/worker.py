import signal
import setproctitle

from ...share.log import logger
from ...share.utils import safe_call


class Worker:

    app = None

    # 是否有效(父进程中代表程序有效，子进程中代表worker是否有效)
    enabled = True

    _got_first_request = False
    # 是否已经发送KeyboardInterrupt
    _got_keyboard_interrupt = False

    _conn = None

    def __init__(self, app):
        self.app = app

    def run(self):
        setproctitle.setproctitle(self.app.make_proc_name('worker'))

        self._handle_signals()

        self._on_worker_start()

        self._conn = self.app.connection_class(
            self, (self.app.host, self.app.port), self.app.conn_timeout
        )

        try:
            self._conn.run()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur. app: %s', self, exc_info=True)
        finally:
            self._on_worker_stop()

    def _on_worker_start(self):
        self.app.events.start_worker(self)
        for bp in self.app.blueprints:
            bp.events.start_app_worker(self)

    def _on_worker_stop(self):
        for bp in self.app.blueprints:
            bp.events.stop_app_worker(self)
        self.app.events.stop_worker(self)

    def _handle_signals(self):
        def stop_handler(signum, frame):
            safe_stop_handler(signum, frame)

            # 防止重复发送KeyboardInterrupt
            # 因为在终端直接CTRL-C是会自动往子进程发送的
            # 但是kill -INT不会
            if not self._got_keyboard_interrupt:
                self._got_keyboard_interrupt = True
                raise KeyboardInterrupt

        def safe_stop_handler(signum, frame):
            self.enabled = False

            # 关闭读，从而快速退出
            safe_call(lambda: self._conn.shutdown(0))

        # 强制结束，抛出异常终止程序进行
        signal.signal(signal.SIGINT, stop_handler)
        # 安全停止
        signal.signal(signal.SIGTERM, safe_stop_handler)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)

    def __repr__(self):
        return '<%s name: %s>' % (
            type(self).__name__, self.app.name
        )
