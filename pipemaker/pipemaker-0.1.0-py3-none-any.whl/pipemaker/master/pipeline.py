import subprocess
import shlex
import os
from queue import Queue
from time import sleep
from importlib import reload

import pipemaker.master as m
from ..utils.share import create_server, create_client
from ..qrabbit import pika
from ..web import view
from .basepipeline import BasePipeline
from ..worker import Workers
import logging

log = logging.getLogger(__name__)


class Pipeline(BasePipeline):
    """ adds multiprocessing to base pipeline
    """

    def __init__(self):
        super().__init__()
        self._lock = False

        self.mode = "s"
        self.n_workers = os.cpu_count()

        # set on start
        self.taskdb = None
        self.taskq = None
        self.taskqP = None
        self.ch = None
        self.workers = None
        self.pipeline = None
        self.filehandler = None

        self._lock = True

    @property
    def mode(self):
        """ s=sync, a=async """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """ start multiprocessing when set to async """
        if mode == "s":
            pass
        elif mode == "a":
            if self.taskq is None:
                self.start()
        else:
            raise Exception("Invalid mode. Must be s (sync) or a (async)")
        self._mode = mode

    def wait(self, url):
        if not self.taskq:
            log.error("to use multiprocessing please install rabbitmq and run start()")
            return
        m.Eventq(url).start()

    def start(self):
        """ start log, web view, taskq, workers
        """
        # web server thread. takes time so start early
        view.start()

        log.info(m.CONFIG)

        if m.CONFIG.qtype == "qrabbit":
            # enable rabbitmq connection to be shared by logqP, taskdb.workerqP, taskqP, taskq.workerqP
            if not self.ch or self.ch.is_closed:
                self.ch = pika.get_channel(
                    heartbeat=0, client_properties=dict(connection_name="pipeline"),
                )
        else:
            # servers
            log.info("starting servers")
            m.Workerq.start_server()
            m.Taskq.start_server()
            m.Eventq.start_server()
            create_server(Queue(), port=logging.handlers.DEFAULT_TCP_LOGGING_PORT)
            # wait until all running
            while True:
                try:
                    for port in [
                        m.CONFIG.taskq_port,
                        m.CONFIG.workerq_port,
                        m.CONFIG.eventq_port,
                        logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                    ]:
                        create_client(port=port)
                    break
                except ConnectionRefusedError:
                    log.info("waiting")
                    sleep(1)
            log.info("python queue servers running")

        ch = self.ch

        # logging
        log.info(f"starting logging")
        self.filehandler = m.loghandler.FileHandler(
            os.path.expanduser("~") + "/pipemaker.log"
        )
        rootlog = logging.getLogger()
        rootlog.addHandler(m.loghandler.SharedQueueHandler(ch=ch))

        # taskq consumer thread
        log.info(f"starting taskq")
        self.taskdb = m.TaskDB(ch=ch)
        self.taskq = m.Taskq(self.taskdb)
        self.taskqP = m.TaskqP(ch=ch)

        # workerq consumer processes
        if self.n_workers > m.CONFIG.max_workers:
            log.warning(f"Limited to {m.CONFIG.max_workers} workers by config file")
            self.n_workers = m.CONFIG.max_workers
        self.workers = Workers(self.n_workers, ch=ch)
        self.workers.start()

    def stop(self):
        """ close log, web view, taskq, workers; and delete temp files """
        # close web server
        log.info("stopping flask server")
        view.stop()

        # close taskq
        if self.taskq:
            log.info("stopping taskq")
            self.taskq.stop()
            self.taskq = None

        # close worker processes
        if self.workers:
            log.info("stopping workers")
            self.workers.stop()
            self.workers = None

        # delete temporary files
        log.info("deleting temp files")
        self.cleanup()

        # reset logging to remove any queue handlers before deleting queues
        self.filehandler.close()
        self.filehandler = None
        rootlog = logging.getLogger()
        rootlog.removeHandler(rootlog.handlers[-1])

        # delete queues
        if m.CONFIG.qtype == "qrabbit":
            if not self.ch or self.ch.is_closed:
                self.ch = pika.get_channel(
                    heartbeat=0, client_properties=dict(connection_name="pipeline_stop")
                )
            ch = self.ch
            for q in ["Workerq", "Taskq", "Logq", "Eventq"]:
                ch.queue_delete(q)
            ch.connection.close()
            self.ch = None

    def kill(self):
        """ restart local rabbitmq server deleting all queues.
        
        .. warning:: this is the nuclear option for testing
        """

        def subprocess_run(cmd):
            cmd = shlex.split(cmd)
            subprocess.run(cmd, capture_output=True, check=True, shell=True)

        log.info("restarting rabbitmq broker")
        subprocess_run("rabbitmqctl stop_app")
        subprocess_run("rabbitmqctl reset")
        subprocess_run("rabbitmqctl start_app")

    # taskdb functions ###########################################################

    def view(self):
        """ view taskdb """
        df = None
        try:
            df = self.taskdb.view()
        except:
            return "Unable to get taskdb"
        if df is None:
            return "Taskdb is empty"

        # remove prefix from url for files in default location
        prefix = f"{self.fs}/{self.root}/"
        df.url = df.url.apply(lambda x: x[len(prefix) :] if x.startswith(prefix) else x)
        df = df.rename(columns=dict(url="path"))
        return df

    def reset(self):
        super().reset()

        # apply any changes to config.yaml e.g. change in broker
        reload(m)

        if self.taskdb is not None:
            self.taskdb.clear()

    # def set_priority(self, taskid, priority):
    #     self.taskqP.set_priority(taskid, priority)
    #
    # def terminate(self, taskid):
    #     """ terminate task. if running then also restarts worker  """
    #     self.taskqP.set_status(taskid, "terminated")
    #     self.start_workers()
    #
    # def to_waiting(self, taskid):
    #     """ pause task. if running then also restarts worker """
    #     self.taskqP.set_status(taskid, "waiting")
    #     self.start_workers()
    #
    # def to_ready(self, taskid):
    #     """ unpause task that was previously paused; or restart task that failed """
    #     self.taskqP.set_status(taskid, "ready")
