
NAME = 'peony'

# 系统返回码
# 命令字不合法
RET_INVALID_CMD = -10000
# 系统内部异常
RET_INTERNAL = -10001
# admin用户验证失败
RET_ADMIN_AUTH_FAIL = -20000
# master连接未连接
RET_MASTER_NOT_CONNECTED = -21000


# 管理员命令
# 获取运行状态统计
CMD_ADMIN_SERVER_STAT = 20000

# 停止整个server
CMD_ADMIN_STOP = 21003


DEFAULT_CONFIG = {
    'HOST': '127.0.0.1',
    'PORT': 9250,

    # 启动的worker_id闭区间。
    'WORKER_ID_BEGIN': None,
    'WORKER_ID_END': None,

    # 通过task路由worker_id:
    #    def worker_router(task):
    #        return worker_id
    'WORKER_ROUTER': lambda task: 1,

    'DEBUG': False,

    # task class
    'TASK_CLASS': 'maple.task.Task',

    # master class
    'MASTER_CLASS': 'peony.master.Master',

    # proxy class
    'PROXY_CLASS': 'peony.proxy.Proxy',

    # worker class
    'WORKER_CLASS': 'peony.worker.Worker',

    'NAME': NAME,

    # 每个worker的消息队列的最大长度, <=0 代表无限
    'TASK_QUEUE_MAX_SIZE': -1,

    # backlog
    'BACKLOG': 256,

    # 客户端连接超时
    'CLIENT_TIMEOUT': None,

    'STOP_TIMEOUT': None,

    # 处理task超时(秒). 超过后会打印fatal日志. None 代表永不超时
    'WORK_TIMEOUT': None,

    # 管理员，可以连接proxy获取数据
    # 管理员访问地址: 'admin.sock' or ('127.0.0.1', 9910)
    'ADMIN_ADDRESS': 'admin.sock',
    'ADMIN_USERNAME': None,
    'ADMIN_PASSWORD': None,
}
