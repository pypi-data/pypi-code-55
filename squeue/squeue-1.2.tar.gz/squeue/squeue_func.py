"""
squeue: A simple SQLite Queue
"""
from uuid import uuid1
from .squeue import SqliteQueue, loads, dumps

__JOB_QUEUE_FILE = 'jobs.sqlite'
__JOB_QUEUE = SqliteQueue(__JOB_QUEUE_FILE)
__JOB_QUEUE_KEY_FORMAT = 'job:result:%s'

def queue_function(func, queue=__JOB_QUEUE):
    "Queue a function for future processing."
    def delay(*args, **kwargs):
        "Enqueue function Queue and return queueId."
        key = __JOB_QUEUE_KEY_FORMAT % str(uuid1())
        value = dumps((func, key, args, kwargs))
        queue.enqueue(value)
        return key
    func.delay = delay
    return func

def dequeue_function(queue=__JOB_QUEUE, sleep_wait=False):
    "Dequeue and execute next unit for processing."
    return_value = queue.dequeue(sleep_wait=sleep_wait)
    if not return_value:
        return return_value
    func, _, args, kwargs = loads(return_value)
    try:
        return_value = func(*args, **kwargs)
    except Exception as exception:
        return_value = exception
    return return_value
