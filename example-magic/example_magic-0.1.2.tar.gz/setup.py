from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="example_magic",
    version="0.1.2",
    author="Bartosz Telenczuk and IPython Development Team",
    author_email="bartosz@telenczuk.pl",
    description="Example IPython magic extension (used for testing)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/btel/example_magic",
    packages=find_packages(),
    classifiers=[
        "Framework :: IPython",
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.1'
)
