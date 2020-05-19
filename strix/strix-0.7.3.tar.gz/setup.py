import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strix",
    version="0.7.3",
    author="HFM3",
    # author_email="author@example.com",
    description="A Python Package for field-based GIS work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/HFM3/strix',
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    python_requires='>=3.8',
)

# https://github.com/pypa/sampleproject/blob/master/setup.py
