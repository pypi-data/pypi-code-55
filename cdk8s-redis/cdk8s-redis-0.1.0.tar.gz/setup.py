import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk8s-redis",
    "version": "0.1.0",
    "description": "redis constructs for cdk8s",
    "license": "Apache-2.0",
    "url": "https://github.com/eladb/cdk8s-redis.git",
    "long_description_content_type": "text/markdown",
    "author": "Elad Ben-Israel<benisrae@amazon.com>",
    "project_urls": {
        "Source": "https://github.com/eladb/cdk8s-redis.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_redis",
        "cdk8s_redis._jsii"
    ],
    "package_data": {
        "cdk8s_redis._jsii": [
            "cdk8s-redis@0.1.0.jsii.tgz"
        ],
        "cdk8s_redis": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.5.0, <2.0.0",
        "publication>=0.0.3",
        "cdk8s>=0.20.0, <0.21.0",
        "constructs>=2.0.1, <3.0.0"
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
