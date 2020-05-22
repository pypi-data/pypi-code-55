import threading 
from .logAggregator import LogAggregator
from .models.log import Log
from .models.returnLog import ReturnLog
from .models.stat import Stat

class LlamaLogs:
    globalAccountKey = ''
    globalGraphName = ''

    @staticmethod
    def init(options):
        try:
            LlamaLogs.globalAccountKey = str(options["accountKey"])
            LlamaLogs.globalGraphName = str(options["graphName"])

            commThread = threading.Thread(target=LogAggregator.start_timer)
            commThread.daemon = True
            commThread.start()
        except:
            print("`LlamaLogs Error: init function")

    @staticmethod
    def point_stat(options):
        try:
            options["type"] = "point"
            LlamaLogs.processStat(options)
        except:
            print("LlamaLogs Error: point_stat function")

    @staticmethod
    def avg_stat(options):
        try:
            options["type"] = "average"
            LlamaLogs.processStat(options)
        except:
            print("LlamaLogs Error: avg_stat function")

    @staticmethod
    def max_stat(options):
        try:
            options["type"] = "max"
            LlamaLogs.processStat(options)
        except:
            print("LlamaLogs Error: max_stat function")

    @staticmethod
    def log(options, returnLog = None):
        try:
            return LlamaLogs.processLog(options, returnLog)
        except:
            print("LlamaLogs Error: log function")
            traceback.print_exc()

    @staticmethod
    def force_send(options):
        try:
            LogAggregator.send_messages()
        except:
            print("LlamaLogs Error: force_send function")

    @staticmethod
    def processStat(options):
        stat = Stat()
        stat.component = options["component"]
        stat.name = options["name"]
        stat.value = options["value"]
        stat.type = options["type"]

        if ("accountKey" in options):
            stat.account = options["accountKey"]
        else:
            stat.account = LlamaLogs.globalAccountKey or -1 

        if ("graphName" in options):
            stat.graph = options["graphName"]
        else:
            stat.graph = LlamaLogs.globalGraphName
        
        LogAggregator.add_stat(stat)

    @staticmethod
    def processLog(options, returnLog):
        if (returnLog is not None):
            options["s"] = returnLog.sender
            options["r"] = returnLog.receiver
            options["initialMessage"] = returnLog.initialMessage
            options["startTime"] = returnLog.startTime
            options["acountKey"] = returnLog.accountKey
            options["graphName"] = returnLog.graphName

        log = Log()
        if ("s" in options):
            log.sender = options["s"]
        else:
            log.sender = options["sender"]

        if ("r" in options):
            log.receiver = options["r"]
        else:
            log.receiver = options["receiver"]
        
        log.log = options["log"]

        if ("error" in options):
            log.error = (options["error"] and True) or False

        if ("accountKey" in options):
            log.account = options["accountKey"]
        else:
            log.account = LlamaLogs.globalAccountKey or -1 

        if ("graphName" in options):
            log.graph = options["graphName"]
        else:
            log.graph = LlamaLogs.globalGraphName

        if ("initialMessage" in options):
            log.initialMessage = options["initialMessage"]

        if ("startTime" in options):
            log.elapsed = log.timestamp - options["startTime"]

        LogAggregator.add_log(log)
        return ReturnLog(log)