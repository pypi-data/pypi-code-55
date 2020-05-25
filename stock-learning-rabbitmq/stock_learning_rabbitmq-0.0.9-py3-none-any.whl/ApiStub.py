from stock_learning_rabbitmq.QueueNameConstants import API_QUEUE_NAME
from stock_learning_rabbitmq.Stub import Stub


class ApiStub(Stub):
    
    def __init__(self, server):
        super().__init__(server, 'stock-learning-api')

    def infomoney_ibovespa_initial_load(self, content):
        self._send('infomoney-ibovespa-initial-load', content)

    def infomoney_ibovespa_live_update(self, content):
        self._send('infomoney-ibovespa-live-update', content)
