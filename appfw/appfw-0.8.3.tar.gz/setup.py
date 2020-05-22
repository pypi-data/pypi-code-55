import os
import re
import setuptools

def read(*parts):
    with open(os.path.join(PWD, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^\s*__version__\s*=\s*['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


PWD = os.path.abspath(os.path.dirname(__file__))
PACKAGE = 'appfw'
VERSION = find_version(PACKAGE, '__init__.py')


setuptools.setup(
    name=PACKAGE,
    version=find_version(PACKAGE, '__init__.py'),
    author="Ergin Soysal",
    author_email="esoysal@gmail.com",
    description="Application framework",
    long_description= read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/soysal/appfw",
    packages=setuptools.find_packages(),
    package_data={PACKAGE: ['tpl/*.tpl']},
    entry_points={
        'console_scripts': ['app-init=appfw.app_init:run'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
         "Operating System :: OS Independent",
    ],
)
