import versioneer
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

cur_dir = path.abspath(path.dirname(__file__))

with open(path.join(cur_dir, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='testproject1234',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='hhslepicka',
    packages=find_packages(),
    description='Test Project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hhslepicka/testproject1234',
    license='BSD',
)
