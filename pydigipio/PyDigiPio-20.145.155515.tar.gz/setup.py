import time
import subprocess
from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="PyDigiPio",
    version=time.strftime(
        "%y.%j.%k%M%S",
        time.localtime(
            int(
                subprocess.check_output("git show -s --format='%ct'", shell=True)
                .decode()
                .strip()
            )
        ),
    ),
    description="Python module for Raspberry Pi GPIO",
    long_description_content_type="text/markdown",
    long_description=readme,
    author="Einar Arnason",
    author_email="einsiarna@gmail.com",
    url="https://github.com/EinarArnason/PyDigiPio",
    license="MIT License",
    py_modules=["PyDigiPio"],
    test_suite="tests",
    platforms=["linux"],
)
