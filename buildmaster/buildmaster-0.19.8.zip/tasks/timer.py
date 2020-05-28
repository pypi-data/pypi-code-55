# encoding=utf-8
import sys
import os
from datetime import datetime

sys.path.append('../')  # 使得tasks可被import
os.environ['settings_dir'] = '../'  # 指定buildmaster需要找setting.py，可以在当前目录中另外配置

from tasks import app
from buildmaster.app import db


def load_timer_from_db():
    from celery.schedules import crontab    #调度参数动态eval中使用到
    schedule = {}
    tasks = db.query('select * from task_timer')
    for t in tasks:
        if not t['enabled']:
            t['loadError'] = 'Disabled: 未启动'
            db.merge('task_timer', t)
            continue
        if not t['taskMethod']:
            t['loadError'] = 'taskMethod必须指定'
            db.merge('task_timer', t)
            continue

        s = {
            'task': t['taskMethod']
        }
        if not t['schedule']:
            t['loadError'] = 'schedule必须指定'
            db.merge('task_timer', t)
            continue

        try:
            value = eval(t['schedule'])
            if isinstance(value, crontab):
                s['schedule'] = value
            else:
                t['loadError'] = f"调度Crontab错误: {t['schedule']} 不是Crontab Python表达式"
                db.merge('task_timer', t)
                continue
        except Exception as e:
            t['loadError'] = f"调度Crontab错误: {str(e)}"
            db.merge('task_timer', t)
            continue
        if t['defaultArgs']:
            try:
                s['args'] = eval(t['defaultArgs'])
            except Exception as e:
                t['loadError'] = f"默认参数错误: {str(e)}"
                db.merge('task_timer', t)
                continue
        t['loadError'] = '启动正常'
        t['startTime'] = datetime.now()
        db.merge('task_timer', t)
        schedule[t.name] = s
    return schedule


app.conf.beat_schedule = load_timer_from_db()
