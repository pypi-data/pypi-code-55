from setuptools import setup

def readme():
    with open ('README.md') as f:
        README = f.read()
    return README

setup(
    name ="itarj-console",
    version = "1.0.0",
    description="A python package to register or view fake job alerts",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/startng/forward4-itarj-adekams",
    author="Adenike Salau",
    author_email="kifademi@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['itarj_console'],
    include_package_data = True,
    install_requires = [
        "time",
        "re",
        "os",
    ],
    entry_points = {
        "console_scripts": [
            "itarj-console = itarj_console.itarj:is_this_a_real_job",
        ]
    },
)

