import setuptools
from resolvr import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="resolvr",
    author="TheTwitchy",
    version=VERSION,
    author_email="thetwitchy@thetwitchy.com",
    description="A penetration testing tool to resolve domains and optionally filter on in-scope results.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/TheTwitchy/resolvr",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        "netaddr",
        "requests",
        "termcolor"
    ],
    entry_points = {
        'console_scripts': [
            'resolvr = resolvr.main:main',                  
        ],              
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
    ],
    python_requires='>=3.6',
)
