import os
import re
from setuptools import setup


setup(name='mock-mysql',
      version='0.0.2',
      description='mysqld 服务端模板程序',
      author="Neeky",
      author_email="neeky@live.com",
      maintainer='Neeky',
      maintainer_email='neeky@live.com',
      scripts=['bin/mock-mysql'],
      packages=['mockmysql'],
      python_requires='>=3.8.*',
      )
