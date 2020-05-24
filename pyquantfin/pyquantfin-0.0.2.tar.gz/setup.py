from setuptools import setup

filepath = 'README.md'

setup(name='pyquantfin',
      version='0.0.2',
      description='package for quant finance lecture',
      url='https://pypi.org/manage/projects/',
      author='mortalm',
      author_email='mortalm@sina.com',
      packages=['pyquantfin'],
      long_description=open(filepath, encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      package_data={
       '': ['data/assets.csv','data/hs300.csv','data/*.h5','data/sp500.xlsx']}
)
