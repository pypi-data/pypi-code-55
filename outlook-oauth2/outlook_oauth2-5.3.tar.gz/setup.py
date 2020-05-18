import setuptools

from outlook_oauth2 import __release__

setuptools.setup(
    name='outlook_oauth2',
    version=__release__,
    packages=['outlook_oauth2', 'outlook_oauth2.internal', 'outlook_oauth2.core'],
    url='https://gitlab.com/alexbishop/pyOutlook',
    license='MIT',
    author='Alex Bishop',
    author_email='alexbishop1234@gmail.cpm',
    description='This is a fork of pyOutlook (https://pypi.python.org/pypi/pyOutlook) with support for multiple mailboxes.',
    install_requires=['requests', 'python-dateutil'],
    keywords='outlook office365 microsoft email'
)
