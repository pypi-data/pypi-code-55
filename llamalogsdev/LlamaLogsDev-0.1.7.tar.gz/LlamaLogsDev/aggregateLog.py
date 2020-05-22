import json
from LlamaLogsDev.helpers import ms_time

class AggregateLog:
    def __init__(self, log):
        self.sender = log.sender
        self.receiver = log.receiver
        self.account = log.account
        self.log = ''
        self.errorLog = ''
        self.initialMessageCount = 0
        self.graph = log.graph
        self.total = 0
        self.errors = 0
        self.elapsed = 0
        self.elapsedCount = 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def toAPIFormat(self):
        api_log = {}
        api_log["sender"] = self.sender
        api_log["receiver"] = self.receiver
        api_log["count"] = self.total
        api_log["errorCount"] = self.errors
        api_log["log"] = self.log
        api_log["errorLog"] = self.errorLog
        api_log["clientTimestamp"] = ms_time()
        api_log["graph"] = self.graph or 'noGraph'
        api_log["account"] = self.account
        api_log["initialMessageCount"] = self.initialMessageCount
        return api_log