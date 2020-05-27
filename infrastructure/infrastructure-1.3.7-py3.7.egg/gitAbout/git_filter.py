# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-25 16:43:44
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-05-26 20:00:06
import platform
class GitFilter(object):
	"""
		git项目过滤
	"""
	def __init__(self,serviceCodeDir):
		self.serviceCodeDir = serviceCodeDir


	def get_backslash(self):
		sysstr = platform.system()
		if sysstr =="Windows":
			return "\\"
		else:
			return '/'

	def filter_jarName(self):
		for name in os.listdir(self.serviceCodeDir):
			name_path = self.serviceCodeDir + self.get_backslash() + name
			if name == '.git':
				continue
			elif 'iface' in name.lower():
				continue
			elif os.path.isdir(name_path):
				for file in os.listdir(name_path):
					file_path = name_path + self.get_backslash() + file
					if os.path.isfile(file_path) and file == "pom.xml":
						pass


if __name__ == '__main__':
	a=GitFilter('gea')
	print(a.get_backslash())
