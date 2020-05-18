import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class efshandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create EFS client
            self.efs_client = session.client('efs', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create EFS client', {'region': self.region})

        self.file_systems = self.describe_file_systems()

    def describe_file_systems(self):
        file_systems = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.efs_client.describe_file_systems(Marker = response['Marker'])
                else:
                    response = self.efs_client.describe_file_systems()

                file_systems.extend(response['FileSystems'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call EFS describe_file_systems', {'region': self.region})

            if 'Marker' not in response:
                break

        return file_systems

    def efs_encryption_not_enabled(self):
        failures = []
        for file_system in self.file_systems:
            delete_state = ['deleting', 'deleted']
            if file_system['LifeCycleState'] not in delete_state:
                if not file_system['Encrypted']:
                    failures = self.helper.append_item_to_list(failures, 'efs', file_system['FileSystemId'], file_system['FileSystemId'] , self.region)
        
        return failures

    def efs_not_encrypted_with_kms_cmk(self):
        failures = []
        for file_system in self.file_systems:
            delete_state = ['deleting', 'deleted']
            if file_system['LifeCycleState'] not in delete_state:
                if not file_system['Encrypted']:
                    failures = self.helper.append_item_to_list(failures, 'efs', file_system['FileSystemId'], file_system['FileSystemId'] , self.region)
                else:
                    key_details = self.helper.get_kms_key_details(file_system['KmsKeyId'])
                    if key_details['KeyManager'] != 'CUSTOMER':
                        failures = self.helper.append_item_to_list(failures, 'efs', file_system['FileSystemId'], file_system['FileSystemId'] , self.region)
        
        return failures