import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="usinelib",
    version="0.0.1",
    author="Martin Bergman",
    author_email="martin@devsed.se",
    description="Fetch menu from usine.se",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/misse/usinelib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
