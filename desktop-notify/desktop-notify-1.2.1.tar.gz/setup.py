
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = 'desktop-notify',
	version = '1.2.1',
	python_requires = '>=3.8',
	install_requires = [
		'dbus-next>=0.1.3',
	],
	entry_points = {
		'console_scripts': [
			'desktop-notify = desktop_notify:run',
		],
	},
	author = 'hxss',
	author_email = 'hxss@ya.ru',
	description = 'Util for sending desktop notifications over dbus.',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://gitlab.com/hxss/desktop-notify',
	packages = setuptools.find_packages(),
	classifiers = [
		'Programming Language :: Python :: 3.8',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX :: Linux',
		'Topic :: Utilities',
	],
)
