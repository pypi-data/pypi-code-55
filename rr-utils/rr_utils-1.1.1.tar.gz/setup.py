import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rr_utils',
    version='1.1.1',
    description="""It is a set of useful classes for python. """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RobertOlechowski/RR_Utils_Python',
    author='Robert Olechowski',
    author_email='RobertOlechowski@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    zip_safe=False,
    scripts=[],
	install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )
