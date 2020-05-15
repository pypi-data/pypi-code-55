import setuptools

from version import get_git_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ni-consumers-core",
    version=get_git_version(),
    author="Primael Bruant",
    author_email="primael.bruant@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pika==1.1.0",
        "requests==2.23.0",
        "coloredlogs==14.0",
        "click==7.1.2",
        "ni-logging-utils==0.0.3"
    ],
    entry_points='''
       [console_scripts]
       consumer=consumers_core.cm:cm
    ''',
    python_requires='>=3.6'
)
