import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-solutions-konstruk.core",
    "version": "0.8.1",
    "description": "Core CDK Construct for patterns library",
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
        "aws_solutions_konstruk.core",
        "aws_solutions_konstruk.core._jsii"
    ],
    "package_data": {
        "aws_solutions_konstruk.core._jsii": [
            "core@0.8.1.jsii.tgz"
        ],
        "aws_solutions_konstruk.core": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.5.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-apigateway>=1.40.0, <1.41.0",
        "aws-cdk.aws-cloudfront>=1.40.0, <1.41.0",
        "aws-cdk.aws-cloudwatch>=1.40.0, <1.41.0",
        "aws-cdk.aws-cognito>=1.40.0, <1.41.0",
        "aws-cdk.aws-dynamodb>=1.40.0, <1.41.0",
        "aws-cdk.aws-elasticsearch>=1.40.0, <1.41.0",
        "aws-cdk.aws-events>=1.40.0, <1.41.0",
        "aws-cdk.aws-iam>=1.40.0, <1.41.0",
        "aws-cdk.aws-iot>=1.40.0, <1.41.0",
        "aws-cdk.aws-kinesis>=1.40.0, <1.41.0",
        "aws-cdk.aws-kinesisanalytics>=1.40.0, <1.41.0",
        "aws-cdk.aws-kinesisfirehose>=1.40.0, <1.41.0",
        "aws-cdk.aws-kms>=1.40.0, <1.41.0",
        "aws-cdk.aws-lambda>=1.40.0, <1.41.0",
        "aws-cdk.aws-lambda-event-sources>=1.40.0, <1.41.0",
        "aws-cdk.aws-logs>=1.40.0, <1.41.0",
        "aws-cdk.aws-s3>=1.40.0, <1.41.0",
        "aws-cdk.aws-sns>=1.40.0, <1.41.0",
        "aws-cdk.aws-sqs>=1.40.0, <1.41.0",
        "aws-cdk.core>=1.40.0, <1.41.0"
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
