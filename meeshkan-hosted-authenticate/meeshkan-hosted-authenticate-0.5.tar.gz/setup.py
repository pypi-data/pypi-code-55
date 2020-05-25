import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()


setup(
    name="meeshkan-hosted-authenticate",
    version="0.5",
    description="Utility package to to verify firebase access tokens on meeshkan.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meeshkan/meeshkan-hosted-authenticate",
    author="Meeshkan Dev Team",
    author_email="dev@meeshkan.com",
    license="MIT",
    packages=["meeshkan_hosted_authenticate"],
    zip_safe=False,
    install_requires=["firebase-admin", "meeshkan-hosted-secrets==0.5"],
)
