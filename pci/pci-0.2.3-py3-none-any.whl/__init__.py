# coding=utf-8

from pci.enodebfunction import *
from pci.PCI_App import *

def pci():
    root = tk.Tk()
    root.geometry("400x200+10+10")
    root.title("PCI@广东电信综维优中心片区 Version0.2.3")
    root.minsize(400, 200)
    app = Application(root)
    root.mainloop()

def main():
    pci()

def init():
    pci()

#module level doc-string
__doc__ = """
@File：__init__.py
@Date：2020-05
@Version: 0.2.3
@Author: zhongjie
@Desc：评估PCI组的复用距离


pci@Version: 0.2.3
-----------------------------------------------------------------------

Introduction
-----------------------------------------------------------------------
	[1] 评估PCI group;
	[2] 地理化呈现评估结果
	[3] 提供测距/自定义矢量图层等基本功能

	
Package Install
-----------------------------------------------------------------------
	python_requires=">=3.5"

Import File Format
-----------------------------------------------------------------------
	导入文件要求：
	    [1] csv格式文件;
	    [2] 至少包括以下几个列名的列：'enodebid','cellid','pci', 'longitude', 'latitude', 'city', 'cellname'.
	
	其他要求：
	    [1] 经纬度：请遵循经纬度的有效范围输入有效值，但程序中暂时没有加以限制;
	    [2] PCI组：请遵循PCI组号的有效范围0至167的整数，但程序中暂时没有加以限制.


Example Usage
-----------------------------------------------------------------------
以下提供两种用法

.. code:: python

	from pci import *
	pci() / main() / init()

.. code:: python

	import pci
	pci.pci() / pci.main() / pci.init()
	
Help Document
-----------------------------------------------------------------------
	
.. code:: python

	import pci
	help(pci)


LICENSE
--------
See LICENSE.txt file.
	



"""
