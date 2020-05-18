import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="contractor-jwt-lib",
    version="0.0.7",
    author="Daniel Gellman",
    description="Internal library for managing JWTs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['certifi==2020.4.5.1',
                        'chardet==3.0.4',
                        'ecdsa==0.15',
                        'idna==2.9',
                        'okta-jwt==1.3.5',
                        'pyasn1==0.4.8',
                        'python-jose==3.1.0',
                        'requests==2.23.0',
                        'rsa==4.0',
                        'six==1.14.0',
                        'urllib3==1.25.9',
],
    include_package_data=True,
    zip_safe=False
)