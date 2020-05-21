import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-solutions-konstruk.aws-lambda-dynamodb",
    "version": "0.8.1",
    "description": "CDK Constructs for AWS Lambda to AWS DynamoDB integration.",
    "license": "Apache-2.0",
    "url": "https://github.com/awslabs/aws-solutions-konstruk.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/awslabs/aws-solutions-konstruk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_solutions_konstruk.aws_lambda_dynamodb",
        "aws_solutions_konstruk.aws_lambda_dynamodb._jsii"
    ],
    "package_data": {
        "aws_solutions_konstruk.aws_lambda_dynamodb._jsii": [
            "aws-lambda-dynamodb@0.8.1.jsii.tgz"
        ],
        "aws_solutions_konstruk.aws_lambda_dynamodb": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.5.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-dynamodb>=1.40.0, <1.41.0",
        "aws-cdk.aws-lambda>=1.40.0, <1.41.0",
        "aws-cdk.core>=1.40.0, <1.41.0",
        "aws-solutions-konstruk.core>=0.8.1, <0.9.0",
        "constructs>=3.0.2, <4.0.0"
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
