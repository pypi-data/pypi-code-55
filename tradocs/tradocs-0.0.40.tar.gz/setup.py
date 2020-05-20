from setuptools import setup, find_packages
from distutils.command.install_data import install_data

with open('README.md', 'r') as fh:
    long_description = fh.read()

cmdclasses = {'install_data': install_data}
data_files = [('config', ['config/tradocs.json'])]

REQUIREMENTS = [
    'Click',
    'configparser',
    'translate-toolkit',
    'lxml',
    'requests',
    'colorama',
]

CLASSIFIERS = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
]

setup(
    name='tradocs',
    version='0.0.40',
    author='Eber Rodrigues',
    author_email='eberjoe@gmail.com',
    description='DocFX localization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/eberjoe/ui-docs-zanata-md',
    license = 'MIT',
    packages = find_packages(),
    cmdclasses = 'cdmclass',
    data_files = 'data_files',
    entry_points = {
        'console_scripts': ['tradocs = tradocs.tradocs:root']
    },
    classifiers = CLASSIFIERS,
    install_requires = REQUIREMENTS,
    python_requires='>=3.6',
)