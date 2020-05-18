import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class fsxhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create FSx client
            self.fsx_client = session.client('fsx', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create FSx client', {'region': self.region})

        self.file_systems = self.describe_file_systems()

    def describe_file_systems(self):
        file_systems = []
        response = {}
        while True:
            try:
                if 'NextToken' in response:
                    response = self.fsx_client.describe_file_systems(NextToken = response['NextToken'])
                else:
                    response = self.fsx_client.describe_file_systems()

                file_systems.extend(response['FileSystems'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call FSx describe_file_systems', {'region': self.region})

            if 'NextToken' not in response:
                break
        
        return file_systems

    def fsx_not_using_kms_cmk(self):
        failures = []

        for file_system in self.file_systems:
            try:                
                response = self.helper.get_kms_key_details(file_system['KmsKeyId'])
                if response['KeyManager'] != 'CUSTOMER' : 
                    failures = self.helper.append_item_to_list(failures, 'fsx', file_system['FileSystemId'], file_system['ResourceARN'] , self.region)
            
            except Exception as e:
                self.logger.error(f"Error while getting kms key details for file system - { file_system['FileSystemId'] }: {e}")
            
        return failures
