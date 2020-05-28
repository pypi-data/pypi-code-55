import pipemaker.master as m
from pipemaker.filesystem import Filepath
import pandas as pd
from datetime import datetime
import logging

log = logging.getLogger(__name__)


class TaskDB:
    """ Handles events that update the database of tasks
    """

    # dict(url=task) of running tasks including waiting, running, completed, failed
    tasks = dict()

    def __init__(self, ch=None):
        self.ch = ch
        self.workerqP = m.WorkerqP(ch=ch)

        # number of tasks in workerq or being processed by workers
        self.submitted = 0

    # messages from workers ####################################################

    def onRun(self, body):
        """ new tasks arrive here as dict(url=task) including upstream tasks """
        for k, v in body["tasks"].items():
            # if already scheduled then just add in the new downstream task
            current = self.tasks.get(k)
            if current:
                # finished tasks can be replaced and rerun
                if current.status in [
                    "completed",
                    "terminated",
                    "failed",
                    "failed_upstream",
                ]:
                    self.tasks.pop(k)
                # unfinished tasks can have additional downstream tasks added
                else:
                    current.downstream = current.downstream | (v.downstream)
                    continue
            v.status = "waiting"
            self.tasks[k] = v
            if not v.upstream:
                v.status = "ready"
        self.submit()

    def onRunning(self, body):
        """ finished loading data and started processing """
        task = self.tasks[body["source"]]
        task.status = "running"

    def onProgress(self, body):
        """ handles event fired by task to show progress """
        task = self.tasks[body["source"]]
        task.progress = int(body["progress"])

    def onComplete(self, body):
        """ task has completed and all output has been written """
        # update the task on data and release any downstream
        task = self.tasks[body["source"]]
        task.status = "completed"
        task.finished = body["time"]
        task.progress = 100
        task.details = ""

        # run any tasks that can now run
        for d in task.downstream:
            dtask = self.tasks[d]
            dtask.upstream.remove(task.url)
            if not dtask.upstream:
                dtask.status = "ready"
        task.downstream = set()

        # notify complete if there are consumers already but don't wait.
        if self.ch:
            m.EventqP(task.url, ch=self.ch.connection.channel())
        else:
            m.EventqP(task.url)

        self.submitted -= 1
        self.submit()

    def onError(self, body):
        task = self.tasks[body["source"]]
        task.status = "failed"
        task.details = str(body["exception"])

        def fail_downstream(task):
            """ recursively fail all downstream tasks """
            for d in task.downstream:
                dtask = self.tasks[d]
                dtask.status = "failed_upstream"
                dtask.details = str(task)
                fail_downstream(dtask)

        fail_downstream(task)

        self.submitted -= 1
        self.submit()

    def onLoading(self, body):
        """ task has been received by a workertask and is loading the data before processing """
        task = self.tasks[body["source"]]
        task.status = "loading"
        task.pid = body["pid"]
        task.process = body["process"]
        task.started = body["time"]
        task.finished = None

    def onSaving(self, body):
        """ task has finished and output is being saved """
        task = self.tasks[body["source"]]
        task.status = "saving"

    # direct functions #################################################################################

    def submit(self):
        """ submit tasks to workerq """
        n = m.CONFIG.max_workerq - self.submitted
        df = self.view()
        if len(df) == 0:
            return
        for task in df[df.status == "ready"].url[:n]:
            self.tasks[task].status = "workerq"
            self.workerqP.put(self.tasks[task].workertask)
            self.submitted += 1

    def view(self):
        """ get tasks and format as dataframe
        :return: dataframe of tasks
        """
        if len(self.tasks) == 0:
            return None

        # format tasks
        df = pd.DataFrame.from_dict([t.__dict__ for t in self.tasks.values()])
        cols = [
            "url",
            "name",
            "status",
            "priority",
            "pid",
            "process",
            "started",
            "finished",
            "elapsed",
            "remaining",
            "progress",
            "details",
        ]
        for col in set(cols) - set(df.columns):
            df[col] = None

        df.started = pd.to_datetime(df.started, errors="coerce")
        df.finished = pd.to_datetime(df.finished, errors="coerce")

        # calculated columns
        started = df.started.fillna(datetime.now())
        finished = df.finished.fillna(datetime.now())
        df["elapsed"] = (finished - started).dt.total_seconds() // 60
        df["remaining"] = df.elapsed / df.progress * 100 - df.elapsed
        if "upstream" in df.columns:
            # for waiting tasks set details=upstream
            df.loc[df.status == "waiting", "details"] = df.upstream.apply(
                lambda upstream: ",".join([str(self.tasks[url]) for url in upstream])
            )

        # not running
        df.loc[df.started.isnull(), "elapsed"] = None
        df.loc[df.started.isnull() | df.finished.notnull(), "remaining"] = None

        # formatting
        df.progress = df[df.progress.notnull()].progress.apply(
            lambda x: str(int(x)) + "%"
        )
        df.started = df.started[df.started.notnull()].dt.strftime("%H:%M")
        df.finished = df.finished[df.finished.notnull()].dt.strftime("%H:%M")
        df.elapsed = df.elapsed[df.elapsed.notnull()].astype(int).apply(str)
        df.remaining = df.remaining[df.remaining.notnull()].astype(int).apply(str)
        df = df[cols].fillna("").sort_values("started", ascending=False)
        return df

    def clear(self):
        """ clear pipeline of all tasks """
        self.tasks.clear()

    def get_task(self, taskid):
        """ convert taskid to task """
        if isinstance(taskid, int):
            df = self.view()
            url = df.loc[taskid].url
        elif isinstance(taskid, str):
            url = Filepath(taskid).url

        task = self.tasks.get(url, None)
        if task is None:
            raise Exception(f"Task not found {task}")
        return task


##### not possible to change "ready" tasks as they are already in the workerqP
# def set_priority(self, taskid, priority):
#     """ set priority for task. tasks are selected for execution in priority order """
#     raise NotImplementedError
#     task = self.get_task(taskid)
#     task.priority = priority
#
# def set_status(self, taskid, status):
#     """ set status of task including downstream tasks. terminate process if running.
#     :param taskid: index|url
#     :param status: terminated|waiting!ready
#     """
#     raise NotImplementedError
#     task = self.get_task(taskid)
#
#     # remove upstream reference
#     for upstream in task.upstream:
#         self.tasks[upstream].downstream.remove(task.url)
#
#     # terminate process if task is running
#     if task.pid and task.status in ["loading", "running", "saving"]:
#         # block other workers from starting this task
#         task.status = status
#         # terminate process. task may continue running and updating status
#         log.info(f"terminating worker for {task.url} on {task.pid} {task.process}")
#         p = psutil.Process(task.pid)
#         p.terminate()
#         p.wait()
#     if not task.status == "completed":
#         task.status = status
#         log.info(f"status={status} for {url}")
#
#     # recursively terminate downstream tasks
#     for downstream in task.downstream.copy():
#         self.terminate(downstream)

# EXAMPLE OF HOW TO REQUEST INFO FROM QUEUE VIA MESSAGE
# def onView(self, body):
#     """ sends unformatted copy of the task queue to body queue
#     :body: dict(key=routing_key). caller uses routing key to match request/body.
#     """
#     key = body["key"]
#     producer.Eventq(key, self.channelP, self.tasks)

# def get_tasks(self):
#     """ get the tasks dict from taskqP. sends message to taskqP; waits for response
#     :return: dict of tasks
#     """
#     # request tasks from taskqP and wait for response
#     key = f"get_tasks {str(uuid4())}"
#     self.put(dict(event="onView", key=key))
#     tasks = consumer.Eventq(key).start(auto_ack=True, timeout=10)
#     return tasks
