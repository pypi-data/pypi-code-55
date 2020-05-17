from setuptools import setup, find_packages
from os import path
from glob import glob

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def data_files():
    files = glob("src/nlpcleaner/data/nltk/**/**/*", recursive=True)
    files = [f for f in files if path.isfile(f)]
    return files

setup(name='nlpcleaner',
      version='0.3.0',
      description='Clean and prepare text for modeling with machine learning',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/giovannelli/nlpcleaner',
      author='Duccio Giovannelli',
      author_email='giovannelli@extendi.it',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      data_files=data_files(),
      install_requires=[
          'regex',
          'nltk >= 3.5',
          'pycld3 >= 0.2.0'
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False,
      classifiers=[
        # See: https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ])
