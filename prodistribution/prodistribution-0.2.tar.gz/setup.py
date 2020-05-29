from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='prodistribution',
    version='0.2',
    description='Gaussian and binomial distributions',
    packages=['prodistribution'],
    zip_safe=False,
    author="Soumitra Edake",
    author_email="souedake@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s0umitra/pypi-prodistribution",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
