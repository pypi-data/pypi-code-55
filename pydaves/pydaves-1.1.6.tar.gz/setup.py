import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydaves",
    version="1.1.6",
    author="Davide Miani",
    author_email="davide.miani2@gmail.com",
    description="Personal utils package for my Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidemiani/pydaves",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
