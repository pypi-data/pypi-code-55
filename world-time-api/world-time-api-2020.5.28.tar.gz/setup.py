import setuptools

with open("README.md",'r') as f:
    long_description = f.read()

setuptools.setup(
    name="world-time-api",
    version='2020.05.28',
    author='Tyler Dula',
    author_email='echo.dulatr@gmail.com',
    description='A wrapper for the World Time API.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dulatr/WorldTimeAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)