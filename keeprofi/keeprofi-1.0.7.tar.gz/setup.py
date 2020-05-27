
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "keeprofi",
	version = "1.0.7",
	python_requires = '>=3.7',
	install_requires = [
		'xdg>=4.0.0',
		'xerox>=0.4.1',
		'pynput>=1.4.2',
		'pykeepass>=3.0.3',
		'keyring>=19.0.1',
		'desktop-notify>=1.2.1'
	],
	entry_points = {
		'console_scripts': [
			'keeprofi = keeprofi:main',
		],
	},
	author = "hxss",
	author_email = "hxss@ya.ru",
	description = "Python util that provide access to keepass database using rofi drun menu.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://gitlab.com/hxss/keeprofi",
	packages = setuptools.find_packages(),
	keywords = ['keepass', 'rofi', 'keyring'],
	classifiers = [
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
		"Topic :: Utilities",
	],
)
