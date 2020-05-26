import sys
from collections import Counter
from netkit.box import Box

from .master import Master
from .worker import Worker
from .worker import Request
from .worker import Connection
from .common.mixins import RoutesMixin, AppEventsMixin
from ..share.log import logger
from ..share import constants


class Application(RoutesMixin, AppEventsMixin):

    ############################## configurable begin ##############################

    # 显示的进程名
    name = constants.NAME

    host = None
    port = None

    # 消息协议类
    box_class = Box
    # master 类
    master_class = Master
    # worker 类
    worker_class = Worker
    # connection 类
    connection_class = Connection
    # request 类
    request_class = Request

    # 调试模式
    debug = False

    # worker数量
    workers = 1

    # 最多回应一次
    rsp_once = True
    # 网络连接超时(秒)，包括 connect once，read once，write once。None 代表不超时
    conn_timeout = None
    # 处理task超时(秒). 超过后worker会自杀. None 代表永不超时
    work_timeout = None
    # 停止子进程超时(秒). 使用 TERM 进行停止时，如果超时未停止会发送KILL信号
    stop_timeout = None

    ############################## configurable end   ##############################

    blueprints = None

    def __init__(self, box_class=None):
        RoutesMixin.__init__(self)
        AppEventsMixin.__init__(self)
        self.blueprints = list()

        if box_class is not None:
            self.box_class = box_class

    def register_blueprint(self, blueprint):
        blueprint.register_to_app(self)

    def run(self, host, port, debug=None, workers=None):
        self._validate_cmds()

        self.host = host
        self.port = port
        if debug is not None:
            self.debug = debug
        if workers is not None:
            self.workers = workers

        logger.info('Connect to gateway. name: %s, address: %s, debug: %s, workers: %s',
                    self.name, (self.host, self.port), self.debug, workers)

        self.master_class(self).run()

    def make_proc_name(self, subtitle):
        """
        获取进程名称
        :param subtitle:
        :return:
        """
        proc_name = '[%s:%s %s] %s' % (
            constants.NAME,
            subtitle,
            self.name,
            ' '.join([sys.executable] + sys.argv)
        )

        return proc_name

    def _validate_cmds(self):
        """
        确保 cmd 没有重复
        :return:
        """

        cmd_list = list(self.rule_map.keys())

        for bp in self.blueprints:
            cmd_list.extend(list(bp.rule_map.keys()))

        duplicate_cmds = list((Counter(cmd_list) - Counter(set(cmd_list))).keys())

        assert not duplicate_cmds, 'duplicate cmds: %s' % duplicate_cmds

    def __repr__(self):
        return '<%s name: %s>' % (
            type(self).__name__, self.name
        )
