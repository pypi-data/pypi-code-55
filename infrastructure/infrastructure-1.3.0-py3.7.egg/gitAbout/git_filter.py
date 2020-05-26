# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-25 16:43:44
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-05-25 17:06:43

class GitFilter(object):
	"""
		git项目过滤
	"""
	def __init__(self,serviceCodeDir):
		self.serviceCodeDir = serviceCodeDir


	def filter_jarName(self):
		for name in os.listdir(self.serviceCodeDir):
			if name == '.git':
				continue
			elif 'iface' in name.lower():
				continue
			# elif os.path.isdir(self.serviceCodeDir.format(service_name=alreadyRecord.service_name) + '/' + name):