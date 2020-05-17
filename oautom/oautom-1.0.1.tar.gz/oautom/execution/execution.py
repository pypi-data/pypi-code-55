# pylint: disable=simplifiable-if-expression
from abc import abstractmethod
from enum import Enum
from typing import List


class ExecutionState(str, Enum):
    disable = 'disable'
    waiting = 'waiting'
    running = 'running'
    done = 'done'


class Execution:

    def __init__(self, name: str, flow: 'Flow'):
        self._name = name
        flow.register_execution(self)
        self._depends = []  # type: List[Execution]
        self._status = ExecutionState.disable

    def depends(self, previous: 'Execution'):
        self._depends.append(previous)

    def name(self):
        return self._name

    def status(self):
        return self._status

    def initialize(self):
        self._status = ExecutionState.waiting

    def run_if_ready(self):
        for dependency in self._depends:
            dependency.check_if_done()

        if self._status == ExecutionState.waiting:
            ready_to_run = True
            for dependency in self._depends:
                ready_to_run &= False if dependency.status() != ExecutionState.done else True

            if ready_to_run:
                self.run()
                return True

        return False

    @abstractmethod
    def run(self):
        self._status = ExecutionState.running

    def check_if_done(self):
        if self.check():
            self._status = ExecutionState.done

    @abstractmethod
    def check(self) -> bool:
        raise NotImplementedError()
