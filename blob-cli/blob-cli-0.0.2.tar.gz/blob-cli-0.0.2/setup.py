from setuptools import setup, find_packages

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

setup(
    name='blob-cli',
    version='0.0.2',
    author='Hsueh-Hung Cheng',
    author_email='jhengsh.email@gmail.com',
    url='https://github.com/Jhengsh/blob-cli',
    description='Azure Blob Shell Command',
    scripts=[
        'blob_cli/bin/blob_list', 'blob_cli/bin/blob_tier',
        'blob_cli/bin/blob_delete', 'blob_cli/bin/blob_upload',
        'blob_cli/bin/blob_download'
    ],
    long_description=open('README.rst').read().strip(),
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    license='MIT',
    platforms='any',
    python_requires='!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=["azure-storage-blob"],
)
