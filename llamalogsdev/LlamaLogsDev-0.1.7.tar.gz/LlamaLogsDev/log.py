from LlamaLogsDev.helpers import ms_time

class Log:
    def __init__(self):
        self.sender = ''
        self.receiver = ''
        self.timestamp = ms_time()
        self.log = ''
        self.initialMessage = True
        self.account = ''
        self.graph = ''
        self.error = False
        self.elapsed = 0