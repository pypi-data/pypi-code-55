from setuptools import setup

setup(
   name='mdict-py',
   version='0.1a1',
   description='Python API for mdict IO (MDX and MDD).',
   author='oxdc',
   author_email='projaias@outlook.com',
   url='https://github.com/oxdc/mdict.py',
   packages=[
      'mdict',
      'mdict.core',
      'mdict.ciphers'
   ],
   install_requires=[]
)
