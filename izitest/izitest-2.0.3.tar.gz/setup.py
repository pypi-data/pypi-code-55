from setuptools import (setup, find_packages)

with open("README.rst", 'r') as f:
    readme = f.read()

with open("requirements.txt", 'r') as f:
    requirements = f.read()

setup(
    name="izitest",
    version="2.0.3",
    author="Kenji 'Nhqml' Gaillac",
    author_email="kenji.gaillac@epita.fr",
    license="GNU GPLv3",
    description="An easy test suite",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://izitest.rtfd.io",
    project_urls={
        "Source": "https://github.com/nhqml/izitest",
        "Documentation": "https://izitest.rtfd.io"
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "izitest": [
            "py.typed",
            "jinja2/*",
        ],
    },
    platforms=[
        "Any",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements.splitlines(),
)
