from setuptools import setup, find_packages
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="oneiot-scheduler",
    version="0.0.1",
    author="Louis Irwin",
    author_email="coding@louisirwin.co.uk",
    description="OneIoT Scheduler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lirwin3007/OneIoT-Scheduler",
    packages=find_packages(),
    python_requires='>=3.6',
    scripts=[
        'scripts/iot-schedule'
    ],
    install_requires=[
        'oneiot-core',
        'apscheduler',
    ]
)
