"""Setup specifications for gitignore project."""

from os import path

from setuptools import setup


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="auto-gitignore",
    version="1.0.0",
    description="Create gitignore template with autocompletion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mux-Mastermann/gitignore",
    author="Jan Knorr",
    license='MIT',
    author_email="jan.hhc+dev@gmail.com",
    py_modules=["gitignore"],
    entry_points={
        "console_scripts": [
            "gitignore = gitignore:main"
        ]
    },
    install_requires=[
        "requests",
        "prompt-toolkit"
    ]
)
