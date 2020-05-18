import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class ssmhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create SSM client
            self.ssm_client = session.client('ssm', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create SSM client', {'region': self.region})

        self.parameters = self.describe_parameters()

    def describe_parameters(self):
        parameters = []
        response = {}

        while True:

            try:
                if 'NextToken' in response:
                    response = self.ssm_client.describe_parameters(NextToken = response['NextToken'])
                else:
                    response = self.ssm_client.describe_parameters()

                parameters.extend(response['Parameters'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Backup describe_parameters', {'region': self.region})

            if 'NextToken' not in response:
                break

        return parameters

    def ssm_paramters_not_encrypted(self):
        failures = []
        for parameter in self.parameters:
            if parameter['Type'] != 'SecureString':
                failures = self.helper.append_item_to_list(failures, 'ssm', parameter['Name'], parameter['Name'] , self.region)
        
        return failures