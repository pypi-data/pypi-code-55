from setuptools import setup

setup(
    name='pywiface',
    version='0.2',
    packages=['pywiface'],
    url='',
    license='MIT',
    author="Keane O'Kelley",
    author_email='keane.m.okelley@gmail.com',
    description='Python wrapper for managing wireless interfaces',
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
