from vect import Vect


class Flow:

    def __init__(self, name: str, app: 'OAutom'):
        self._name = name
        self._executions = []
        app.register_flow(self)

    def name(self):
        return self._name

    def register_execution(self, execution: 'Execution'):
        self._executions.append(execution)

    def vect(self):
        vect = Vect(self._name, self._executions)
        return vect
