# -*- coding: UTF-8 -*-
import os

import pyhdfs

HADOOP_COMMAND_PATH = '/home/ubuntu/emr-hadoop-clis/hadoop/hadoop/bin/hadoop'

"""
通过Hadoop命令对hdfs目录进行操作
"""


class HadoopCommand(object):
    def __init__(self, path, command=HADOOP_COMMAND_PATH):
        self.command = command
        self.path = path

    def remove(self):
        command_line = "{} fs -rm -r {}".format(self.command, self.path)
        print(command_line)
        os.system(command_line)

    def mkdir(self):
        command_line = "{} fs -mkdir -p {}".format(self.command, self.path)
        print(command_line)
        os.system(command_line)

    def is_path_exist(self):
        command_line = "{} fs -test -e {}".format(self.command, self.path)
        print(command_line)
        os.system(command_line)
        if os.system('echo $?') != 0:
            raise Exception("create hdfs failed，please retry")
        return True

    def is_file_exist(self):
        command_line = "%s fs -count %s |awk '{print $2}' " % (self.command, self.path)
        print(command_line)
        p = os.popen(command_line)
        ret = p.read()
        p.close()
        if not ret or ret == '0':
            return False
        else:
            return True

    def chmod(self):
        command_line = "{} fs -chmod -R 777 {}".format(self.command, self.path)
        print(command_line)
        os.system(command_line)

    # 更新path
    def set(self, path):
        self.path = path
        return self


"""
通过pyhdfs命令对hdfs目录进行操作
"""


class HdfsCommand(object):
    def __init__(self, hosts, path, user_name='hadoop'):
        self.fs = pyhdfs.HdfsClient(
            hosts=hosts,
            user_name=user_name)
        self.path = path

    def remove(self):
        self.fs.delete(self.path)

    def mkdir(self):
        self.fs.mkdirs(self.path)

    def is_path_exist(self):
        self.fs.exists(self.path)

    def is_file_exist(self):
        res = self.fs.get_content_summary(self.path)
        if res.spaceConsumed == 0:
            return False
        else:
            return True
