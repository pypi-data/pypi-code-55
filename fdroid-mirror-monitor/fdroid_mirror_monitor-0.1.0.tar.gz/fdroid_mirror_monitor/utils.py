#!/usr/bin/env python3

# stdlibs:
from queue import Queue
import json
import os
import threading
# external:
from fdroidserver import net


def parallelize(list_of_stuff, function_that_does_stuff, num_worker_threads=1):
    """
    Parallelize a loop that iterates over a list and calls a function.

    :param list_of_stuff: (list of) parameter for the function call
    :param function_that_does_stuff: function that gets called with the corresponding parameter
    :param num_worker_threads: number of maximal threads in parallel
    :return: unsorted dict of parameter values with corresponding return value
    """
    return_values = []
    parameter_values = []

    def worker(q):
        while not q.empty():
            stuff = q.get()
            threading.currentThread().name = stuff
            return_value = function_that_does_stuff(stuff)
            return_values.append(return_value)
            parameter_values.append(stuff)
            print(threading.currentThread().name, 'Exiting')
            q.task_done()

    jobs = Queue()
    for stuff in list_of_stuff:
        jobs.put(stuff)

    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(jobs,))
        t.start()
    jobs.join()
    return dict(zip(parameter_values, return_values))


def add_reports_to_history(reports, timestamp, output_path,
                           history_url='https://fdroid.gitlab.io/mirror-monitor/report.json'):
    """
    Download historical reports.
    Append reports to history and save under path

    :param reports: dict
    :param timestamp: save report in history under this timestamp
    :param history_url: source url of history
    :param output_path: output path of concatenated reports
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    content, _ignored = net.http_get(history_url)
    history = json.loads(content.decode())
    history[timestamp] = reports
    with open(output_path, 'w') as fp:
        json.dump(history, fp)
