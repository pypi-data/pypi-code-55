# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-25 17:10:22
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-05-27 10:36:16
import time
class OperateServer(object):
	def __init__(self,remoteServer):
		"""
			操作远程服务器
		"""
		self.remoteServer = remoteServer


	def checkServerStatus(self,service_name,status,coverageLog):
		command = "cd /workspace/carkey/{service_name}/latest;./init.script status".format(service_name=service_name)
		result = self.remoteServer.exec_command(command=command)
		time.sleep(3)
		print(result)
		if status in result[0]:
			record = coverageLog(data=
					{
						"operationType": "检查服务器状态是否符合预期",
						"message": str(result),
						"remark": status,
						"typeInfo": "覆盖率桥接",
						"status":1
					})					
			record.is_valid(raise_exception=True)
			record.save()
			return True
		else:
			return False

	def restartServer(self,service_name,coverageLog):
		stopCommandList = ["sudo su - deploy\n",
		"sudo su\n",
		"cd /workspace/carkey/{service_name}/latest\n".format(service_name=service_name),
		"sudo ./init.script stop\n"]
		while self.checkServerStatus(service_name,'stopped',coverageLog):
			stopResult = self.remoteServer.exec_command(command=restartCommandList)
			record = coverageLog(data=
					{
						"operationType": "统计静态代码停止服务器结果",
						"message": stopResult,
						"typeInfo": "覆盖率桥接",
						"status":1
					})					
			record.is_valid(raise_exception=True)
			record.save()

		
		time.sleep(5)
		startCommandList = ["sudo su - deploy\n",
		"sudo su\n",
		"cd /workspace/carkey/{service_name}/latest\n".format(service_name=service_name),
		"sudo ./init.script start\n"]
		while self.checkServerStatus(service_name,'running',coverageLog):
			restartResult = self.remoteServer.exec_command(command=startCommandList)		
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
