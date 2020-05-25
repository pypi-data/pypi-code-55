import rclpy
from rclpy.executors import Executor, SingleThreadedExecutor, MultiThreadedExecutor, Task
from typing import Callable, Coroutine, List, Type, TypeVar, Union
from concurrent import futures
from . import behavior

TB = TypeVar('TB', bound='Behavior')


class Engine():

    def __init__(self):
        self.spinning = False
        self.behaviors: List[behavior.Behavior] = []
        self.main_executor: Executor = None
        self.co_executor: Executor = None
        rclpy.init()

    def execute(self, callback: Union[Callable, Coroutine], main_thread: bool = True) -> Task:
        return self.main_executor.create_task(callback) if main_thread else self.co_executor.create_task(callback)

    def spin(self, max_threads: int = 1):
        if self.spinning:
            return
        self.spinning = True
        tasks = []
        self.main_executor = SingleThreadedExecutor()
        self.co_executor = MultiThreadedExecutor(max_threads)
        try:
            while self.spinning:
                for beh in self.behaviors:
                    if not beh._inited and beh.enabled:
                        beh._inited = True
                        self.co_executor.add_node(beh)
                        beh.on_enable()
                        tasks.append(self.execute(lambda b=beh: b.on_start()))
                    elif beh._update and beh.enabled:
                        tasks.append(self.execute(lambda b=beh: b.on_update()))
                while any(not t.done() for t in tasks):
                    self.main_executor.spin_once(0)
                    self.co_executor.spin_once(0)
                tasks.clear()
        finally:
            self.shutdown()

    def shutdown(self):
        if not self.spinning:
            return
        self.spinning = False
        for beh in self.behaviors:
            beh.enabled = False
            beh.on_destory()
            beh._engine = None
        self.behaviors = []
        self.main_executor.shutdown()
        self.co_executor.shutdown()

    def spawn_behavior(self, klass: Type[TB]) -> TB:
        beh = klass()
        beh._engine = self
        self.behaviors.append(beh)
        beh.on_awake()
        return beh

    def destory_behavior(self, beh: 'Behavior'):
        if beh not in self.behaviors:
            return
        if beh._inited:
            beh.enabled = False
            beh.on_destory()
            self.co_executor.remove_node(beh)
        self.behaviors.remove(beh)
        beh._engine = None
