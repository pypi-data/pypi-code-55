import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trace-time-glaiel",  # Replace with your own username
    version="0.0.2",
    author="glaiel",
    description="A package providing timer tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glaiel/trace_time",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires='>=3.6',
)
