# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-25 17:10:22
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-05-26 20:08:37
import time
class OperateServer(object):
	def __init__(self,remoteServer):
		"""
			操作远程服务器
		"""
		self.remoteServer = remoteServer


	def checkServerStatus(self,service_name):
		command = "cd /workspace/carkey/{service_name}/latest;./init.script status".format(service_name=service_name)
		result = self.remoteServer.exec_command(command=command)
		time.sleep(3)
		if "running" in result[0]:
			return True
		else:
			return False

	def restartServer(self,service_name):
		restartCommandList = ["sudo su - deploy\n",
		"sudo su\n",
		"cd /workspace/carkey/{service_name}/latest\n".format(service_name=service_name),
		"sudo ./init.script restart\n"]
		while self.checkServerStatus(service_name):
			restartResult = self.remoteServer.exec_command(command=restartCommandList)
		return restartResult

	def addJacocoArg(self,service_name,port):
		commandList = ["sudo su - deploy\n",
		"cd /workspace/carkey/{service_name}/latest\n".format(service_name=service_name),
		"""sudo sed -i -e '1i START_OPTS="$START_OPTS -javaagent:/usr/local/jacoco/jacocoagent.jar=includes=*,output=tcpserver,address=*,port={port},append=true"' init.script\n""".format(
			port=port)]
		result = self.remoteServer.exec_command(command=commandList)
		return result

	def __del__(self):
		self.remoteServer.close()
