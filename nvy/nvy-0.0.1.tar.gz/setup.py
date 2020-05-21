import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nvy",
    version="0.0.1",
    author="Koen Woortman",
    author_email="koensw@outlook.com",
    description="CLI the the Python venv module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license='MIT',
    entry_points={
        'console_scripts': [
            'nvy = nvy:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Environment :: Console',
    ],
)
