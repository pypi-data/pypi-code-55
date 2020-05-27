import datetime
class Uptime:
    def uptimeset():
        global start_time
        start_time = datetime.datetime.utcnow()
        return (start_time)

    def uptime():
        return datetime.datetime.utcnow() - start_time
