from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="taskwatcher",
    version="1.7",
    author="Cedric GUSTAVE",
    author_email="cgustave@free.fr",
    description="Package taskwatcher",
	long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cgustave/taskwatcher",
    packages=find_packages(),
    classifiers=[
	    "Development Status :: 4 - Beta",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
		"Natural Language :: English",
		"Topic :: System :: Networking",
    ],
    python_requires='>=3.5',
)

