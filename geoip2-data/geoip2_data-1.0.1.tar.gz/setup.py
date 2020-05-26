import os
import sys
from setuptools import setup


_here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(_here, 'geoip2_data', 'version.py')) as f:
    exec(f.read(), version)


setup(
    name='geoip2_data',
    version=version['__version__'],
    description=('Show how to structure a Python project.'),
    author='SoundOn',
    author_email='dev@soundon.fm',
    url='https://github.com/SoundOn/geoip2-data',
    license='MIT',
    packages=['geoip2_data'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
    )