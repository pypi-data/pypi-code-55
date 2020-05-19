import sys
from setuptools import setup

if "sdist" not in sys.argv:
    print(
        "You probably meant to install 'elastic-apm'\n"
        "Try running: $ python -m pip install elastic-apm"
    )
    sys.exit(1)

setup(
    name="elasticapm",
    version="0",
    description="Typo-squatting protection for the 'elastic-apm' package",
    url="https://github.com/elastic/apm-agent-python",
    license="BSD License (BSD)",
    author="Elastic",
    author_email="support@elastic.co"
)
