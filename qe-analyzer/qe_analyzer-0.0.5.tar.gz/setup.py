import setuptools
with open("README.md", "r") as fh:
	long_description=fh.read()
	
setuptools.setup(
    name="qe_analyzer", # Replace with your own username
    version="0.0.5",
    author="Elizabeth Pogue",
    author_email="epogue1@jhu.edu",
    description="A small package for analyzing quantum espresso outputs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/euclidmenot2/qe_analyzer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)