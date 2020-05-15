import setuptools
import trace_time


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trace-time-glaiel",  # Replace with your own username
    version=trace_time.__version__,
    author=trace_time.__author__,
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
