# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_error_utils']
install_requires = \
['botocore']

setup_kwargs = {
    'name': 'aws-error-utils',
    'version': '1.0.1',
    'description': 'Error-handling functions for boto3/botocore',
    'long_description': "# aws-error-utils\n**Making botocore.exceptions.ClientError easier to deal with**\n\nAll AWS service exceptions are raised by `boto3` as a `ClientError`, with the contents of the exception indicating what kind of exception happened.\nThis is not very pythonic, and the contents themselves are rather opaque, being held in a dict rather than as properties.\nThe functions in this package help dealing with that.\n\nThe package is on PyPI but I tend to prefer just copying the `aws_error_utils.py` file into my projects, often then my only dependency is on boto3, which is usually somewhere in my environment anyway (e.g., in a Lambda function). But that's just me.\n\n## `catch_aws_error()`\nThis is probably the most useful function in the package. Make exception catching more natural. You use this function in an `except` statement instead of `ClientError`. The function takes as input error code(s), and optionally operation name(s), to match against the current raised exception. If the exception matches, the `except` block is executed. Usage looks like this:\n\n```python\ntry:\n    s3 = boto3.client('s3')\n    s3.list_objects_v2(Bucket='bucket-1')\n    s3.get_object(Bucket='bucket-2', Key='example')\nexcept catch_aws_error('NoSuchBucket', operation_name='GetObject'):\n    # This will be executed if the GetObject operation raises NoSuchBucket\n    # But not if the ListObjects operation raises it\n```\n\nYou can provide error codes either as positional args or as the `code` keyword argument, and there either as a single string or a list of strings.\n\n```python\ncatch_aws_error('NoSuchBucket')\ncatch_aws_error(code='NoSuchBucket')\n\ncatch_aws_error('NoSuchBucket', 'NoSuchKey')\ncatch_aws_error(code=['NoSuchBucket', 'NoSuchKey'])\n```\n\nThe operation name can only be provided as the `operation_name` keyword argument, but similarly either as a single string or a list of strings.\n\nYou must provide an error code. To match exclusively against operation name, use the `aws_error_utils.ALL_CODES` token. There is similarly an `ALL_OPERATIONS` token.\n\n```python\ntry:\n    s3 = boto3.client('s3')\n    s3.list_objects_v2(Bucket='bucket-1')\n    s3.get_object(Bucket='bucket-1', Key='example')\nexcept catch_aws_error(ALL_CODES, operation_name='ListObjectsV2') as e:\n    # This will execute for all ClientError exceptions raised by the ListObjectsV2 call\n```\n\nFor more complex conditions, instead of providing error codes and operation names, you can provide a callable to evaluate the exception:\n\n```python\nimport re\ndef matcher(e):\n    info = get_aws_error_info(e)\n    return re.search('does not exist', info.message)\n\ntry:\n    s3 = boto3.client('s3')\n    s3.list_objects_v2(Bucket='bucket-1')\nexcept catch_aws_error(matcher) as e:\n    # This will be executed if e is a ClientError and matcher(e) returns True\n    # Note the callable can assume the exception is a ClientError\n```\n\n## `get_aws_error_info()`\nThis function takes a returns an `AWSErrorInfo` object, which is a `collections.NamedTuple` with the error code, error message, HTTP status code, and operation name extracted, along with the raw response dictionary. If you're not modifying your code's exception handling, this can be useful instead of remembering exactly how the error code is stored in the response, etc.\n\n## `aws_error_matches()`\nThis is the matching logic behind `catch_aws_error()`. It takes a `ClientError`, with the rest of the arguments being error codes and operation names identical to `catch_aws_error()`, except that it does not support providing a callable.\n",
    'author': 'Ben Kehoe',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benkehoe/aws-error-utils',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
}


setup(**setup_kwargs)
