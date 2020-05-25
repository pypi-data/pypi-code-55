import setuptools


setuptools.setup(
    name="qilum", 
    version="1.0.0",
    author="Damien Loison",
    author_email="loison.damien@gmail.com",
    description="Statistical supplementary package to numpy, scipy, ...",
	long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://www.qilum.com/",
    packages=setuptools.find_packages(),
	keywords="statistic random number generator scipy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires=[
          'numba',
          'numpy',
          'scipy',
      ],
    python_requires='>=3.6',
)
