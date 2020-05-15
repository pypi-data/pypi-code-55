import setuptools
from kabooki.version import version

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="kabooki",
    version=version,
    author="Gilad Kutiel",
    author_email="gilad.kutiel@gmail.com",
    description="Simple Streaming Data Pipeline",
    long_description=long_description,
    url="https://github.com/kabooki/kabooki",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'tqdm'
    ]
)
