import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(name='leetcron',
      version='0.0.6',
      description='Sets up cron job that pushes Leetcode submissions to a Github repository',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/JING1201/leetcron',
      author='jlionwg',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'python-crontab',
          'browsercookie',
          'PyGithub'
      ],
      scripts=['bin/leetcron'],
      zip_safe=False)