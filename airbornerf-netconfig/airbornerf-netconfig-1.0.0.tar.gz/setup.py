from setuptools import setup

setup(
	name='airbornerf-netconfig',
	version='1.0.0',
	description='AirborneRF NetConfig',
	packages=['airbornerf.netconfig', 'airbornerf.netconfig.rf', 'airbornerf.netconfig.types'],
	license='Proprietary',
	author='Thomas Wana',
	author_email='support@airbornerf.com',
	url='https://www.airbornerf.com/',
	install_requires=[
		'sqlalchemy'
	],
)
