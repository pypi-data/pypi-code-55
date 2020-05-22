import schedule
import time
import json

from LlamaLogsDev.llamaProxy import LlamaProxy
from LlamaLogsDev.models.aggregateLog import AggregateLog

class LogAggregator:
    aggregateLogs = {}
    aggregateStats = {}

    @staticmethod
    def start_timer():
        delay = 5
        schedule.every(delay).seconds.do(LogAggregator.send_messages)
        while True:
            schedule.run_pending()
            time.sleep(delay)

    @staticmethod
    def send_messages():
        print("Sent Messages")
        currentLogs = LogAggregator.aggregateLogs
        LogAggregator.aggregateLogs = {}
        currentStats = LogAggregator.aggregateStats
        LogAggregator.aggregateStats = {}
        LlamaProxy.send_messages(currentLogs, currentStats)

    @staticmethod
    def add_log(log):
        if (log.sender not in LogAggregator.aggregateLogs):
            LogAggregator.aggregateLogs[log.sender] = {}
        if (log.receiver not in LogAggregator.aggregateLogs[log.sender]):
            LogAggregator.aggregateLogs[log.sender][log.receiver] = AggregateLog(log)

        working_ob = LogAggregator.aggregateLogs[log.sender][log.receiver]

        if (log.error):
            working_ob.errors = working_ob.errors + 1
        if (log.elapsed):
            prev_amount = working_ob.elapsed * working_ob.elapsedCount
            working_ob.elapsed = (prev_amount + log.elapsed) / (working_ob.total + 1)
            working_ob.elapsedCount = working_ob.elapsedCount + 1
        if (log.initialMessage):
            working_ob.initialMessageCount = working_ob.initialMessageCount + 1

        working_ob.total = working_ob.total + 1
        if (working_ob.log == '' and log.error == False):
            working_ob.log = str(log.log)
        if (working_ob.errorLog == '' and log.error == True):
            working_ob.errorLog = str(log.log)

    @staticmethod
    def add_stat(stat):
        if (stat.type == "point"):
            if (stat.component not in LogAggregator.aggregateStats):
                LogAggregator.aggregateStats[stat.component] = {}
            LogAggregator.aggregateStats[stat.component][stat.name] = stat    

        if (stat.type == "average"):
            LogAggregator.add_stat_avg(stat)
        if (stat.type == "max"):
            LogAggregator.add_stat_max(stat)

    @staticmethod
    def add_stat_avg(stat):
        if (stat.component not in LogAggregator.aggregateStats):
            LogAggregator.aggregateStats[stat.component] = {}
        if (stat.name not in LogAggregator.aggregateStats[stat.component]):
            LogAggregator.aggregateStats[stat.component][stat.name] = stat
            stat.count = 1

        existing = LogAggregator.aggregateStats[stat.component][stat.name]
        existing.value = existing.value + stat.value
        existing.count = existing.count + 1
    
    @staticmethod
    def add_stat_max(stat):
        if (stat.component not in LogAggregator.aggregateStats):
            LogAggregator.aggregateStats[stat.component] = {}
        if (stat.name not in LogAggregator.aggregateStats[stat.component]):
            LogAggregator.aggregateStats[stat.component][stat.name] = stat

        existing = LogAggregator.aggregateStats[stat.component][stat.name]
        if (stat.value > existing.value):
            existing.value = stat.value
