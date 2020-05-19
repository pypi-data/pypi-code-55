from setuptools import setup, find_packages

with open("README.md", "r") as fh:
	readme_description = fh.read()

desc = 'A light-weight (out-of-the box) tool for pushing SQL (MySQL and SQLite) queries, a markup-language for structured txt files and running data loggers in python.'

setup(
	name = 'pyquicksql',
	packages = find_packages(),
	version = '1.1.1',
	license = 'MIT',
	description = desc,
	author = 'Gabriel Cordovado',
	author_email = 'gabriel.cordovado@icloud.com',
	long_description = readme_description,
	long_description_content_type = 'text/markdown',
	url ='https://github.com/GabeCordo/python-quick-sql',
	download_url = 'https://github.com/GabeCordo/python-quick-sql/archive/v_2.1.tar.gz',
	keywords = ['MYSQL', 'SQLITE', 'LOGGING'],
	install_requires = [
		'cffi',
		'pymysql',
		'cryptography'
	],
	classifiers = [
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
	python_requries = '>=3.4',
)