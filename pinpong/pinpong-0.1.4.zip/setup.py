# -*- coding: utf-8 -*-  

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pinpong',
    packages=['pinpong','pinpong/base','pinpong/libs','pinpong/examples'],
    install_requires=['pyserial'],

    include_package_data=True,

    version='0.1.4',
    description="a middleware based on Firmata protocol and compatible with micropython API",
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    python_requires = '>=3.5.*',
    author='Ouki Wang',
    author_email='ouki.wang@dfrobot.com',
    url='https://github.com/DFRobot/pinpong',
    download_url='https://github.com/DFRobot/pinpong',
    keywords=['Firmata', 'Arduino', 'Protocol', 'Python'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

