#! /usr/bin/env python3
# -*- coding:utf-8 -*-
'''
if_service_exists(): Boolean：服务是否存在
if_service_running(): Booleans:服务是否运行
start_run_service(): 无法以admin运行
'''
import os, subprocess, time
import ctypes, sys
# from tool import bat
import zhangwei_helper.function.Os as self_os
import zhangwei_helper.enum.SelfEnum as self_enum

def if_service_exists(service='MySQL'):
    task = subprocess.Popen('sc query state= all | find /i "DISPLAY_NAME: %s"'
                            % service,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True)
    if len(task.stdout.readlines()) == 0:
        return False
    else:
        return True

def if_service_running(service='MySQL'):
    task = subprocess.Popen('tasklist /nh | find /i "%s"' % service,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True)
    if len(task.stdout.readlines()) == 0:
        return False
    else:
        return True


# def start_run_service(service='MySQL'):
#     '''
#     非admin无法启动service
#     :param service:
#     :return:
#     '''
#     cmd = 'net start %s' % service
#     if self_os.windows_login_as_admin():
#         # 将要运行的代码加到这里
#         # if not win_check_mysql_running():
#         subprocess.Popen(cmd,
#                          stdin=subprocess.PIPE,
#                          stdout=subprocess.PIPE, shell=True)
#     else:
#         if self_os.get_python_major_version() == self_enum.PythonVersion.Python3:
#             # subprocess.Popen("runas /savecred /user:Administrator cmd",
#             #                  shell=True)
#             ctypes.windll.shell32.ShellExecuteW(None, "runas",
#                                                 sys.executable, cmd, None, 1)
#             # time.sleep(10)


# if if_service_exists('mysql'):
#     if not if_service_running('mysql'):
#         start_run_service('mysql')