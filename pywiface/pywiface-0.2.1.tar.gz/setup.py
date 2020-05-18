from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pywiface',
    version='0.2.1',
    packages=['pywiface'],
    url='',
    license='MIT',
    author="Keane O'Kelley",
    author_email='keane.m.okelley@gmail.com',
    description='Python wrapper for managing wireless interfaces',
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'pywiface=pywiface.cli:main'
        ]
    },
    install_requires=[
        'scapy-python3',
        'termcolor'
    ]
)
