from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
	long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
	requirements = f.read().strip().split()

setup(
	name='elcano',
	version='0.1.0',
	author='Juan C. Roldán',
	author_email='juancarlos@sevilla.es',
	description='Visual dataset explorer',
	long_description=long_description,
	long_description_content_type='text/markdown',
	install_requires=requirements,
	url='https://github.com/juancroldan/elcano',
	packages=find_packages(),
	package_data={},
	include_package_data=True,
	classifiers=[
		'Development Status :: 1 - Planning',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Programming Language :: Python :: 3',
	],
)
