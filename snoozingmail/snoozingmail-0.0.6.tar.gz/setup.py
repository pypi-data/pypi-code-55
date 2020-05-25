import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snoozingmail",
    version="0.0.6",
    author="Nick Is Snoozin",
    author_email="snoozinforabrusin@gmail.com",
    description="A minimal python3 wrapper for the Gmail API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nknaian/snoozingmail",
    packages=setuptools.find_packages(),
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)