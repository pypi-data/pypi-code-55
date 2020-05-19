from setuptools import setup, find_packages
import os
import sys

if sys.version_info[0] < 3:
    with open('README.md') as f:
        long_description = f.read()
else:
    with open('README.rmd', encoding='utf-8') as f:
        long_description = f.read()


setup(
    name='ssm-simple-cli',
    version='0.1.0',
    license='MIT',
    description = 'A simplistic CLI that works with AWS Systems Manager Parameter Store',
    long_description = long_description,
    long_description_content_type='text/markdown',
    author='Eyal Stoler',
    author_email='eyalstoler@gmail.com',
    url='https://github.com/eyalstoler/ssm-simple-cli',
    download_url='https://github.com/eyalstoler/ssm-simple-cli/archive/v0.1.0.tar.gz',
    keywords=['python', 'cli', 'aws-cli', 'ssm', 'ssm-cli'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'boto3',
        'pyperclip'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points='''
        [console_scripts]
        ssm=cli.src.ssm_cli:cli
    ''',
)