from collections import defaultdict


class StatCounter(object):

    """
    统计计算类
    """

    # 客户端连接数
    clients = 0
    # 客户端请求数
    client_req = 0
    # 客户端回应数
    client_rsp = 0
    # worker请求数
    worker_req_counter = None
    # worker丢弃的请求
    worker_req_discard_counter = None

    def __init__(self):
        self.worker_req_counter = defaultdict(int)
        self.worker_req_discard_counter = defaultdict(int)

    def add_worker_req(self, worker_id):
        self.worker_req_counter[worker_id] += 1

    def add_worker_req_discard(self, worker_id):
        self.worker_req_discard_counter[worker_id] += 1
