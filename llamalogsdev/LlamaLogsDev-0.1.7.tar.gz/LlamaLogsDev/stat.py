import json
from LlamaLogsDev.helpers import ms_time

class Stat:
    def __init__(self):
        self.component = ''
        self.name = ''
        self.value = 0
        self.type = ''
        self.account = ''
        self.graph = ''
        self.timestamp = ms_time()
        self.count = 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def toAPIFormat(self):
        return self.__dict__