from subprocess import Popen

from oautom.execution.execution import Execution


class BashExecution(Execution):

    def run(self):
        super().run()
        self._proc = Popen(self._command, shell=True)

    def check(self) -> bool:
        check = False
        if self._proc:
            self._proc.poll()
            check = self._proc.returncode is not None

        return check

    def __init__(self, name, flow: 'Flow', command: str):
        super().__init__(name, flow)
        self._command = command
        self._proc = None  # type: Popen
