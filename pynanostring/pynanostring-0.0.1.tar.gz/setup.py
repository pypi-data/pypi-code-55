import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'README.md')) as fid:
    README = fid.read()


setup(
    name='pynanostring',
    version='0.0.1',
    description='A bioinformatics package to analyze nanostring data',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/leobiscassi/pynanostring',
    author='Léo Biscassi',
    author_email='leo.biscassi@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=['pynanostring'],
    include_package_data=True,
    install_requires=['pandas'],
    entry_points={
        "console_scripts": [
            "pynanostring=pynanostring.__main__:main",
        ]
    },
)