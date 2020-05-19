
"""
封装通过worker_id来访问数据的功能
"""

import multiprocessing
import queue
from ..share.log import logger


class TaskQueueManager(object):
    """
    通过worker_id来区分的queue
    """

    max_size = None
    queue_dict = None

    def __init__(self, worker_id_range, max_size=-1):
        self.max_size = max_size

        self.queue_dict = dict()
        for worker_id in range(worker_id_range[0], worker_id_range[1] + 1):
            self.queue_dict[worker_id] = multiprocessing.Queue(self.max_size)

    def get_queue(self, worker_id):
        """
        获取对应的队列
        :param worker_id:
        :return:
        """
        return self.queue_dict.get(worker_id)

    def put(self, worker_id, item):
        """
        加入item
        如果成功返回True，如果失败返回False
        :param worker_id:
        :param item:
        :return:
        """
        try:
            self.queue_dict[worker_id].put_nowait(item)
            return True
        except queue.Full:
            logger.error(
                'put item fail, queue is full. worker_id: %s, max_size: %s',
                worker_id, self.max_size
            )
            return False
        except:
            logger.error('put item fail, exc occur. worker_id: %s', worker_id, exc_info=True)
            return False

    def put_to_all(self, item):
        """
        向所有队列发送
        :param item:
        :return:
        """
        for q in self.queue_dict.values():
            try:
                q.put_nowait(item)
            except:
                pass

    def get(self, worker_id):
        if self.empty(worker_id):
            return None
        else:
            return self.queue_dict[worker_id].get_nowait()

    def clear(self, worker_id):
        """
        清空
        :param worker_id:
        :return:
        """
        self.queue_dict.pop(worker_id, None)

    def clear_all(self):
        """
        清空所有
        :return:
        """
        self.queue_dict.clear()

    def empty(self, worker_id):
        """
        判断是否是空的
        :param worker_id:
        :return:
        """
        return self.queue_dict[worker_id].empty()

    def qsize(self, worker_id):
        """
        某个队列的size
        :param worker_id:
        :return:
        """
        return self.queue_dict[worker_id].qsize()
