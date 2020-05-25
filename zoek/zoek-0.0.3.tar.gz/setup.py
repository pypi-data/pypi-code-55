from setuptools import setup, find_packages

base_requirements = [
    'Click>=7.0.0',
]

dev_requirements = [
    'pytest',
    'pytest-flake8',
    'pytest-cov',
]

build_requirements = [
    'setuptools>=38.6.0',
    'twine>=1.11.0',
    'wheel>=0.31.0',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="zoek",
    version="0.0.3",
    author="Davey Kreeft, Tein de Vries",
    author_email="dkreeft@xccelerated.io, teindevries@gmail.com",
    description="Command-line utility to search for files and directories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dkreeft/zoek",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=base_requirements,
    extras_require={
        'dev': dev_requirements,
        'build': [dev_requirements, build_requirements],
    },
    entry_points={
        'console_scripts': [
            'zoek = zoek.cli:fetch'
        ]
    }
)
