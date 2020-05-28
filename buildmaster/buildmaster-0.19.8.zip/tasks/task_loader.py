
import sys
import importlib
import os

os.environ['settings_dir'] = '../'  # 指定buildmaster需要找setting.py，可以在当前目录中另外配置

sys.path.append('../')  # 让其他模块能找到app.py
sys.path.append('../modules')   # 加载的模块根目录


from buildmaster.app import settings, log


def load_tasks():
    for m in settings.modules:  # 共用settings中module的task配置
        task = m.get('task')
        if not task:
            continue
        importlib.import_module(task)


load_tasks()

from tasks import app   # 必须import celery对象才能启动worker
for t in app.tasks:
    log.info(t)
