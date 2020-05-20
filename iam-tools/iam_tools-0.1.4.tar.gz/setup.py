from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

exec(open('iam_tools/version.py').read())

setup(
    name='iam_tools',
    description=(
        'The IAM_tools - '
        'a Python package of tools to deal with IAM data.'),
    license='BSD 3-Clause License',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/dlab-indecol/iam_tools.git',
    author='Radek Lonka, Konstantin Stadler',
    author_email='radek.lonka@ntnu.no, konstantin.stadler@ntnu.no',
    version=__version__,  # noqa
    packages=['iam_tools', ],
    package_data={'iam_tools': ['./LICENSE']},
    entry_points={
        'console_scripts':
        ['filter_IAM = iam_tools.filter:main']},
    install_requires=['pandas >= 0.23.0', 'scipy >= 1.0.0'],
    classifiers=[
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3 :: Only',
          'License :: OSI Approved :: BSD License',
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Topic :: Utilities',
          ],
)
