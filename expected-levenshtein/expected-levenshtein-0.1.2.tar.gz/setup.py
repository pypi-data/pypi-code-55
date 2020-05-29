import os
from setuptools import setup, find_packages, Command


__version__ = None
exec(open('expected_levenshtein/version.py').read())


class CleanCommand(Command):
    """
    Custom clean command to tidy up the project root.
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system(
            'rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./htmlcov')


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    author='Nick Noel Machnik',
    author_email='nick.machnik@gmail.com',
    name='expected-levenshtein',
    version=__version__,
    description="""
        Empirical determination of approximate values for
        levenshtein distances between random strings.""",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/nickmachnik/expected-levenshtein.git',
    setup_requires=[
        'setuptools>=18.0',
        'setuptools_scm'
    ],
    use_scm_version=True,
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'numpy>=1.8.0',
        'numba',
        'importlib_resources'
    ],
    cmdclass={
        'clean': CleanCommand
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
