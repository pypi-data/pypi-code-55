import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="rolling_token_auth",
    version="0.1.2",
    author="Alexander Eichhorn",
    author_email="",
    description="Rolling Token verificator & generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexeichhorn/python-rolling-token-auth",
    install_requires=[
        'cryptography>=2.9.0'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)