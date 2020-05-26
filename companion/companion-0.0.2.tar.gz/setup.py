import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="companion",
    version="0.0.2",
    author="Remake AI",
    author_email="iliao@remake.ai",
    description="Companion robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remakeai/kiddo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
