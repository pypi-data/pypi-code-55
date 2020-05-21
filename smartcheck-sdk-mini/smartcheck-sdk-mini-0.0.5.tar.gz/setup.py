import setuptools
import sys
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'requests'
]

setup_options = dict(
    name="smartcheck-sdk-mini", # Replace with your own username
    version="0.0.5",
    author="Brendan Johnson",
    author_email="brendan.johnson@gmail.com",
    description="A lightweight SDK for Trend Micro Smart Check",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnsobm/smartcheck-sdk-mini",
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=install_requires,
    python_requires='>=3.6',
)
if 'py2exe' in sys.argv:
    # This will actually give us a py2exe command.
    import py2exe
    # And we have some py2exe specific options.
    setup_options['options'] = {
        'py2exe': {
            'optimize': 0,
            'skip_archive': True,
            'dll_excludes': ['crypt32.dll'],
            'packages': ['requests',
                         'cloudonecli', 'ConfigParser'],
        }
    }



setup(**setup_options)

