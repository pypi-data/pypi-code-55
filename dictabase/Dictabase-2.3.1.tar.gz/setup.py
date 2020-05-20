from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['dictabase']
print('packages=', packages)

setup(
    name="Dictabase",

    version="2.3.1",
    # 2.3.1 forgot to disable DEBUG
    # 2.3.0 refactored BaseTable into two classes
    # 2.2.2 refactored BaseTable with getter/setter wrappers
    # 2.1.1 bug fix when defining json-able kwargs in New()
    # 2.1.0 can now store json-able types
    # 2.0.0 optimized it all
    # 1.3.2 fixed unnecessary connections to db
    # 1.3.1 optimized
    # 1.3.0 protected against race/conditions in multi-threaded system
    # 1.2.6 added relational mapping
    # 1.2.5 changed README to rst
    # 1.2.4 updated README
    # 1.2.3 added dependencies
    # 1.2.2 changed from module to package
    # 1.2.1 updated readme
    # 1.1 updated readme

    packages=packages,
    install_requires=['dataset'],
    # scripts=['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    # install_requires=['docutils>=0.3'],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     # And include any *.msg files found in the 'hello' package, too:
    #     'hello': ['*.msg'],
    # },

    # metadata to display on PyPI
    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A database interface that mimics a python dictionary.",
    long_description=long_description,
    license="PSF",
    keywords="dictionary database dictabase grant miller sqlalchemy flask sqlite dataset",
    url="https://github.com/GrantGMiller/dictabase",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/dictabase",
    }

    # could also include long_description, download_url, classifiers, etc.
)

# to push to PyPI

# python -m setup.py sdist bdist_wheel
# twine upload dist/*