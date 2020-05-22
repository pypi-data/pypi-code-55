class ReturnLog:
    def __init__(self, log):
        self.sender = log.receiver
        self.receiver = log.sender
        self.initialMessage = False
        self.startTime = log.timestamp
        self.accountKey = log.account
        self.graphName = log.graph