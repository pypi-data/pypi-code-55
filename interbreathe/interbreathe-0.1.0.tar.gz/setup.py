# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages

import interbreathe

long_description = '''
Fixes references that exist outside a particular repo, when breathe is used
to generate documentation for many projects built separately.
'''


setup(
    name='interbreathe',
    version=interbreathe.__version__,
    url='https://github.com/utzig/interbreathe',
    download_url='https://github.com/utzig/interbreathe',
    license='Apache Software License',
    author='Fabio Utzig',
    author_email='fabio.utzig@nordicsemi.no',
    description='A breathe/intersphinx resolver for multi repo projects',
    long_description=long_description,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    # versions known to work!
    install_requires=[
        'Sphinx>=2.4.4,<=3.0.3',
        'breathe>=4.12.4,<4.18.1',
    ],
)
