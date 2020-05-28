from setuptools import setup, find_packages

setup(
    name="eventmonitoring-client",
    version='2.0.0',
    packages=find_packages(),
    install_requires=["requests>=2.18.2", "pytz"],
)
