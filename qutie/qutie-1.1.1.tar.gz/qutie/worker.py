import threading

from .qt import QtCore
from .qt import bind

from .object import Object

__all__ = ['Worker']

@bind(QtCore.QObject)
class Worker(Object):

    def __init__(self, *, target=None, finished=None, failed=None, **kwargs):
        super().__init__(**kwargs)
        self.target = target
        self.finished = finished
        self.failed = failed
        self.__lock = threading.RLock()
        self.__thread = None
        self.__stop_requested = False

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        self.__target = value

    @property
    def finished(self):
        return self.__finished

    @finished.setter
    def finished(self, value):
        self.__finished = value

    @property
    def failed(self):
        return self.__failed

    @failed.setter
    def failed(self, value):
        self.__failed = value

    def start(self):
        with self.__lock:
            if not self.__thread:
                self.__thread = threading.Thread(target=self.__run)
            self.__stop_requested = False
            self.__thread.start()

    def stop(self):
        self.__stop_requested = True

    def join(self):
        try:
            self.__thread.join()
        except AttributeError:
            pass

    @property
    def stopping(self):
        return self.__stop_requested

    @property
    def alive(self):
        with self.__lock:
            if self.__thread:
                return self.__thread.alive()
        return False

    def __run(self):
        try:
            if self.target is None:
                self.run()
            else:
                self.target(self)
        except Exception as e:
            self.emit('failed', e)
        finally:
            with self.__lock:
                self.__stop_requested = False
                self.__thread = None
                self.emit('finished')

    def run(self):
        pass
