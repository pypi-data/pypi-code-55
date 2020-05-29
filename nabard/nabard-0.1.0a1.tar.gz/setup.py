import os
import random

from setuptools import find_packages, setup

setup(
    name="nabard",
    version=os.getenv("VERSION", "") or f"0.0.0.dev{int(random.random() * 10000)}",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    keywords="robot game code nabard",
    url="https://github.com/nabardio/nabard-python",
    license="GPLv3",
    author="Mehdy Khoshnoody",
    author_email="mehdy.khoshnoody@gmail.com",
    description="Utilities to create games and robots for https://nabard.io",
)
