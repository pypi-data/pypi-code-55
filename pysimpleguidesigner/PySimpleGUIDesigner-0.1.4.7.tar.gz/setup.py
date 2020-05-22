import setuptools
import os

my_classifiers = [
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Topic :: Software Development :: Libraries :: Application Frameworks",
		"Topic :: Multimedia :: Graphics",
		"Operating System :: OS Independent",
]

curr_path = os.path.dirname(os.path.abspath(__file__))
# readmefile = os.path.join(curr_path, 'src', "PySimpleGUIDesigner", "README.md")

with open('README.md', "r", encoding='utf-8') as ff:
	long_description = ff.read()

setuptools.setup(
	# start
	url="https://github.com/nngogol/PySimpleGUI_designer",
	entry_points={"console_scripts": ["PySimpleGUIDesigner = PySimpleGUIDesigner.main:cli"]},
	# text
		name="PySimpleGUIDesigner", author="Nikolay Gogol", author_email="nngogol09@gmail.com",
	description="PySimpleGUI designer, that uses transpiler to produce PySimpleGUI code from Qt Designer xml file.",
	long_description=long_description,
	long_description_content_type="text/markdown",
		license='GNU-GPL', version="0.1.4.7", classifiers=my_classifiers,

	#======
	# files
	#======
	packages=setuptools.find_packages('src'),
	package_dir={'': 'src'},
	install_requires=['PySide2>=5.13', 'click>=7.0', 'PySimpleGUI'],
	###========
	### include
	###========
	include_package_data=True, # If set to True, this tells setuptools to automatically include any data files it finds inside your package directories that are specified by your MANIFEST.in file. For more information, see the section below on Including Data Files.
	package_data={
		'': ['*.ui', '*.md', '*.txt', '*.json', '*.py'],
		"PySimpleGUIDesigner": ['*.ui', '*.md', '*.txt', '*.json', '*.py']
	},
)