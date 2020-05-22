#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/13 0:20
# @Author : yangpingyan@gmail.com
import threading
import heapq
import queue
from time import sleep

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._count = 0
        self._cv = threading.Condition()
    def put(self, item, priority=5):
        with self._cv:
            heapq.heappush(self._queue, (-priority, self._count, item))
            self._count += 1
            self._cv.notify()

    def get(self, timeout=None):
        with self._cv:
            while len(self._queue) == 0:
                self._cv.wait(timeout=timeout)
                raise Exception("empty")
            return heapq.heappop(self._queue)[-1]

def thread_test(sec):
    print(f"start {sec}")
    sleep(sec)
    print(f"end {sec}")

if __name__ == '__main__':
    print("Mission start!")
    for i in [20, 10, 5, 1]:
        threading.Thread(target=thread_test, args=(i,)).start()

    print("Mission complete!")

