import setuptools

import countersign

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name="countersign",
    version=countersign.__version__,
    license='MIT',
    packages=setuptools.find_packages(exclude=('tests',)),
    author="Justin Sexton",
    author_email="justinsexton.dev@gmail.com",
    description="Lightweight API that helps consumers generate random passwords and phrases.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JSextonn/countersign.git",
    python_requires='>=3.6',
    keywords=[
        'password',
        'password-generator',
        'library'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
