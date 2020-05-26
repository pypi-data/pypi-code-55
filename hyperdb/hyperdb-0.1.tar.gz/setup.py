from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(name='hyperdb',
      version='0.1',
      description='Uses Tableau server as Hyper database',
      url='http://github.com/storborg/funniest',
      author='Muhammad Hadi',
      author_email='mhadi813@gmail.com',
      license='BSD',
      packages=find_packages(),
      install_requires=required,
      keywords="tableau hyper pandas dataframe google bigquery google cloud storage azure sql azure storage",
      zip_safe=False)