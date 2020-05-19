import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-apex-cname",
    "version": "0.1.4",
    "description": "CDK construct to allow setting an apex record to a cname",
    "license": "ISC",
    "url": "https://github.com/maskerade/cdk-apex-cname.git",
    "long_description_content_type": "text/markdown",
    "author": "Stefan De Figueiredo",
    "project_urls": {
        "Source": "https://github.com/maskerade/cdk-apex-cname.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk-apex-cname",
        "cdk-apex-cname._jsii"
    ],
    "package_data": {
        "cdk-apex-cname._jsii": [
            "cdk-apex-cname@0.1.4.jsii.tgz"
        ],
        "cdk-apex-cname": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.21.2",
        "publication>=0.0.3",
        "aws-cdk.aws-events>=1.39.0, <2.0.0-0",
        "aws-cdk.aws-events-targets>=1.39.0, <2.0.0-0",
        "aws-cdk.aws-iam>=1.39.0, <2.0.0-0",
        "aws-cdk.aws-lambda>=1.39.0, <2.0.0-0",
        "aws-cdk.core>=1.39.0, <2.0.0-0",
        "constructs>=3.0.3, <4.0.0-0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
