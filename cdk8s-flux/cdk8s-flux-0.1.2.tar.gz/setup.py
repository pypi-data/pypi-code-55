import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk8s-flux",
    "version": "0.1.2",
    "description": "cdk8s library ",
    "license": "Apache-2.0",
    "url": "https://github.com/rafaribe/cdk8s-flux.git",
    "long_description_content_type": "text/markdown",
    "author": "Rafael Ribeiro<rafael.ntw@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/rafaribe/cdk8s-flux.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s-flux",
        "cdk8s-flux._jsii"
    ],
    "package_data": {
        "cdk8s-flux._jsii": [
            "cdk8s-flux@0.1.2.jsii.tgz"
        ],
        "cdk8s-flux": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.5.0, <2.0.0",
        "publication>=0.0.3",
        "cdk8s>=0.21.0, <0.22.0",
        "constructs==2.0.1"
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
