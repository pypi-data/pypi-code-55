import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Google Talent Cloud Wrapper Katon Direct",
    version="0.0.4",
    author="Alex VanLaningham",
    author_email="alexv@katondirect.com",
    description="Simple way to use google talent cloud for basic functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        'google.cloud',
        'six',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
