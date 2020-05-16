import setuptools
from setuptools.command.test import test
import sys

try:
    from pytransmission import __version__ as version
except ImportError:
    import re
    pattern = re.compile(r"__version__ = '(.*)'")
    with open('pytransmission/__init__.py') as f:
        version = pattern.search(f.read()).group(1)

# 
# with open("README.md", "r") as fh:
#     long_description = fh.read()


class pytest(test):

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setuptools.setup(
    name='pytransmission',
    version=version,
    author='Dave Chevell',
    author_email='chevell@gmail.com',
    description='A simple Transmission client',
#     long_description=long_description,
#     long_description_content_type="text/markdown",
    url='https://stash.dchevell.com/projects/HT/repos/pytransmission',
    package_data={'pytransmission': ['py.typed']},
    packages=['pytransmission'],
    keywords=['requests', 'transmission'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    install_requires=['requests'],
#     extras_require={
#         ':python_version == "2.7"': ['futures>=3.1.1']
#     },
#     tests_require=['pytest', 'pytest-flask', 'python-coveralls'],
#     test_suite='tests',
#     cmdclass={
#         'test': pytest
#     }
)
