import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    print(requirements)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyARG-dep",
    version="0.0.1",
    author="NexGen Analytics",
    author_email="info@ng-analytics.com",
    description="This repository contains Python packages required by ARG. It is Python 3 compatible only. More details about ARG are available on gitlab.com/AutomaticReportGenerator/arg.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix"
    ],
    python_requires='>=3.7',
    install_requires=[requirements]
)
