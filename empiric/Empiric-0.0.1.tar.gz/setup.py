from setuptools import setup
import setuptools

libName = 'Empiric'
libVersion = '0.0.1'
libUrl = 'https://github.com/mocnik-science/empiric'

with open('./Empiric/__info__.py', 'w') as f:
  f.write('pkgName = \'%s\'\n' % libName)
  f.write('pkgVersion = \'%s\'\n' % libVersion)
  f.write('pkgUrl = \'%s\'\n' % libUrl)

setup(
  name=libName,
  packages=['Empiric', 'Empiric.internal'],
  install_requires=[
    'flask',
    'flask_login',
    'jsonpath-ng',
  ],
  version=libVersion,
  author='Franz-Benjamin Mocnik',
  author_email='mail@mocnik-science.net',
  description='Empiric, the flexible framework for conducting empirical experiments',
  license='GPL-3',
  url=libUrl,
  download_url='',
  keywords=['empirical experiment', 'map', 'framework', 'testing', 'psychology', 'cognition'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3',
  ],
  python_requires='>=3.6',
)
