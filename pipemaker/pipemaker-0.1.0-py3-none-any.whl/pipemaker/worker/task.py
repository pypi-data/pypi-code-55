from ..filesystem.filepath import Filepath
from ..master import TaskqP, loghandler
import inspect
import multiprocessing as mp
from datetime import datetime
import logging

log = logging.getLogger(__name__)


class Task:
    """
    minimal executable that gets passed to task queue

    * load data, run function, save result (all run locally).
    * trigger events to be actioned on master or elsewhere.

    within step and tasks this includes metadata:

    .. table::

        =========== ============================================================================
        column      explanation
        =========== ============================================================================
        job:        job pipe
        status:     waiting, ready,
                    loading, running, saving,
                    completed, failed, failed_upstream
        upstream:   list of urls for upstream tasks not yet completed
        downstream: list of urls for downstream tasks
        details:    only used to display messages e.g. list of upstream tasks, error message.
        process:    name of process on which it ran
        started:    time run started
        finished:   time run finished
        =========== ============================================================================    
    """

    def __init__(self, module, func, inputs, output):
        """
        :param module: name of module
        :param func: name of func
        :param inputs: data or filepaths to be loaded
        :param output: filepath
        """
        # needed to run task
        self.module = module
        self.func = func
        self.inputs = inputs
        self.output = output

        # metadata from tasksdb
        self.job = None
        self.status = None
        self.upstream = None
        self.downstream = None
        self.pid = None
        self.process = None
        self.started = None
        self.finished = None
        self.progress = None

        # set by worker
        self.taskqP = None

    def __str__(self):
        """ function name """
        return str(self.output)

    def __repr__(self):
        """ with class and filesystem """
        return f"Task({self.output.url})"

    @property
    def workertask(self):
        """ clean version of task for execution """
        return Task(self.module, self.func, self.inputs, self.output)

    def run(self):
        """ execute in worker process """
        try:
            self.load()
            self.execute()
            self.save()
            self.onEvent("onComplete")
            return self.outdata
        except Exception as e:
            log.exception(f"exception in {self.output.path}\ne")
            self.onEvent("onError", exception=e)
            return

    def load(self):
        """ load data from filepaths """
        self.onEvent("onLoading")

        # load func
        from importlib import import_module

        module = import_module(self.module)
        self.func_method = getattr(module, self.func)

        # load data
        self.indata = {
            k: v.load() if isinstance(v, Filepath) else v
            for k, v in self.inputs.items()
        }

    def execute(self):
        """ import module and execute function """
        self.onEvent("onRunning")
        self.outdata = self.func_method(**self.indata)

    def save(self):
        """ save data to filepath """
        self.onEvent("onSaving")
        self.output.save(self.outdata)

    def onEvent(self, event, **kwargs):
        """ send event message

        :param event: string e.g. "onError"
        :param kwargs: optional dict of event data e.g. time, process, url
        """
        kwargs = dict(kwargs)
        kwargs["time"] = datetime.now()
        kwargs["event"] = event
        kwargs["pid"] = mp.current_process().pid
        kwargs["process"] = mp.current_process().name
        kwargs["source"] = self.output.url
        self.taskqP.put(kwargs)


# events callled from running task ##################################


def onEvent(event, **kwargs):
    """ fire event from task
    enables onEvent() in one line of code without changing the function signature

    :param event: event to call e.g. "onProgress"
    """
    # minimum 2 steps back to get task reference here=>function=>task
    taskrun = inspect.currentframe().f_back.f_back

    # limited range allows for failure
    for x in range(10):
        try:
            return taskrun.f_locals["self"].onEvent(event, **kwargs)
        except:
            pass
        taskrun = taskrun.f_back
        if taskrun is None:
            break


def progress(i, total):
    """ reports progress from task
    enables progress(10, 100) in one line of code without changing the function signature

    :param i: iteration
    :param total: total iterations at completion
    """
    # add 1 to depth to get from progress to onEvent
    onEvent("onProgress", progress=(i * 100) // total)
