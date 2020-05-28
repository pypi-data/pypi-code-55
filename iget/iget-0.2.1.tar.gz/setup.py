import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iget", # Replace with your own username
    version="0.2.1",
    author="Billow Wang",
    author_email="netheadonline@gmail.com",
    description="A small CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        "console_scripts": [
            "iget = iget.main:get",
        ]
    },
)


# python setup.py sdist
# python setup.py bdist_wheel

# twine upload dist/*