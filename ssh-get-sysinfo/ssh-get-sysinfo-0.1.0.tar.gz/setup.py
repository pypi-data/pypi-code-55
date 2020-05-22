import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = fobj.readlines()
requires = [x.strip() for x in requires]

setup(
    name="ssh-get-sysinfo",
    version="0.1.0",
    description="Get system information via ssh channel.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="info@zencore.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["ssh-get-sysinfo"],
    requires=requires,
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["ssh_get_sysinfo"],
    entry_points={
        "console_scripts": [
            "ssh-get-sysinfo = ssh_get_sysinfo:main",
        ]
    },
)
