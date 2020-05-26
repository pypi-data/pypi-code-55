import setuptools


with open('requirements.txt') as f:
    requirements = f.read().split()

setuptools.setup(
    name='oring',
    version='0.0.1',
    author='kezhang',
    author_email=None,
    license="BSD (3-clause)",
    url="https://github.com/ke-zhang-rd/oring",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)
