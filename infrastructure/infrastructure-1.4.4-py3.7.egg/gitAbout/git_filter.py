# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-25 16:43:44
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-05-28 10:20:15

from infrastructure.parse.parse_xml import ParseXml
# import sys
# sys.path.append("/Users/yongfanmao/哈啰mycode/jc/library/infrastructure")
# from parse.parse_xml import ParseXml
import platform
import os

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
		jarList = []
		sourcePathList = []
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
						px = ParseXml(file_path)
						name = px.get_designation_node("artifactId","project")
						if name:
							jarList.append(name)
							sourcePathList.append(name_path)
					if os.path.isdir(file_path):
						# dspservice 第二层判断
						for sub_file in os.listdir(file_path):
							sub_file_path = file_path + self.get_backslash() + sub_file
							if os.path.isfile(sub_file_path) and sub_file == "pom.xml":
								px = ParseXml(sub_file_path)
								sub_name = px.get_designation_node("artifactId","project")
								if sub_name:
									jarList.append(sub_name)
									sourcePathList.append(file_path)

		return jarList,sourcePathList




if __name__ == '__main__':
	a=GitFilter('/Users/yongfanmao/哈啰mycode/jc/AppHelloAnunnakiDSPService')
	print(a.filter_jarName())
