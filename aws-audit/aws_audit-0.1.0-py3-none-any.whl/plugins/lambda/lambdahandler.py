import json, os
from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class lambdahandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Lambda client
            self.lambda_client = session.client('lambda', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Lambda client', {'region': self.region})

        self.functions = self.list_functions()
    
    def list_functions(self):
        functions = []
        response = {}

        while True:

            try:
                if 'NextMarker' in response:
                    response = self.lambda_client.list_functions(Marker = response['NextMarker'])
                else:
                    response = self.lambda_client.list_functions()

                functions.extend(response['Functions'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Lambda list_functions', {'region': self.region})

            if 'NextMarker' not in response:
                break

        return functions

    def get_policy(self, function_name):
        try:
            response = self.lambda_client.get_policy(FunctionName=function_name)

            return response

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                return {}
            else:
                raise classify_error(self.logger, e, 'Failed to call Lambda get_policy', {'region': self.region})

    def lambda_function_exposed_to_everyone(self):

        failures = []

        for function in self.functions:
            try:
                policy = self.get_policy(function['FunctionName'])
                if policy:
                    policy_document = json.loads(policy['Policy'])
                    is_exposed = self.helper.is_policy_exposed_to_everyone(policy_document)
                    if is_exposed:
                        failures = self.helper.append_item_to_list(failures, 'lambda', function['FunctionName'], function['FunctionArn'] , self.region)            
            except Exception as e:
                self.logger.error(f"Error while getting Lambda policy: {e}")
        
        return failures

    def lambda_function_with_cross_account_access(self):

        failures = []

        for function in self.functions:
            try:
                policy = self.get_policy(function['FunctionName'])
                if policy:
                    policy_document = json.loads(policy['Policy'])
                    is_caa_enabled = self.helper.is_policy_has_cross_account_access(policy_document)
                    if is_caa_enabled:
                        failures = self.helper.append_item_to_list(failures, 'lambda', function['FunctionName'], function['FunctionArn'] , self.region)            
            except Exception as e:
                self.logger.error(f"Error while getting Lambda policy: {e}")
        
        return failures

    def lambda_function_not_in_vpc(self):
        failures = []

        for function in self.functions:
            if 'VpcConfig' not in function:
                failures = self.helper.append_item_to_list(failures, 'lambda', function['FunctionName'], function['FunctionArn'] , self.region)

        return failures
