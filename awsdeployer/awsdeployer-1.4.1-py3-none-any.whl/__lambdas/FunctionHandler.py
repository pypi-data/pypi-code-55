import boto3
import time

from awsdeployer.__lambdas.IamHandler import IamHandler
from awsdeployer.__util import *


class FunctionHandler:
    def __init__(self, aws_config, name, config, layer_handlers):
        self.aws = aws_config
        self.client = boto3.client('lambda',
                                   region_name=self.aws['region'],
                                   aws_access_key_id=self.aws['access_key'],
                                   aws_secret_access_key=self.aws['secret_key'])

        self.name = name
        self.aws_name = self.aws['lambda_prefix'] + '_' + name if self.aws['lambda_prefix'] else name
        self.handler = name + '.lambda_handler'
        self.timeout = config['timeout'] if 'timeout' in config else 3
        self.memory_size = config['memory_size'] if 'memory_size' in config else 128
        self.environment = {
            'Variables': config['env']
        } if 'env' in config else {}

        self.files = [config['main_file'] if 'main_file' in config else name + '.py']
        if 'additional_files' in config:
            self.files += config['additional_files']

        # get dependency layers arns
        self.layer_arns = []
        for layer in layer_handlers:
            arn = layer.get_arn()
            if arn:
                self.layer_arns.append(arn)

    def create(self):
        role_arn = IamHandler(self.aws).create_lambda_role(self.name)
        code = zip_function(self.files)

        time.sleep(10)  # need this for the role to propagate

        response = self.client.create_function(
            FunctionName=self.aws_name,
            Publish=True,
            Runtime=self.aws['runtime'],
            Role=role_arn,
            Handler=self.handler,
            Code={
                'ZipFile': code
            },
            Environment=self.environment,
            Layers=self.layer_arns,
            Timeout=self.timeout,
            MemorySize=self.memory_size
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 201:
            raise RuntimeError

    def update_configs(self, retry=True):
        try:
            response = self.client.update_function_configuration(
                FunctionName=self.aws_name,
                Runtime=self.aws['runtime'],
                Handler=self.handler,
                Environment=self.environment,
                Layers=self.layer_arns,
                Timeout=self.timeout,
                MemorySize=self.memory_size
            )

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise RuntimeError

        except self.client.exceptions.ResourceNotFoundException:
            if retry:
                # create function if it not exists, then retry update configs
                self.create()
                self.update_configs(retry=False)

    def update_code(self, retry=True):
        print('Update function code: {0}'.format(self.name))

        try:
            response = self.client.update_function_code(
                FunctionName=self.aws_name,
                ZipFile=zip_function(self.files),
                Publish=True
            )

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise RuntimeError

        except self.client.exceptions.ResourceNotFoundException:
            if retry:
                # create function if it not exists, then retry update code
                self.create()
                self.update_code(retry=False)




