import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class secretsmanagerhandler : 
    
    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create SECRET_MANAGER client
            self.secretsmanager_client = session.client('secretsmanager', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create SECRET_MANAGER client', {'region': self.region})
        
        
        self.secretsmanager_secrets = self.list_secrets()
        
    def list_secrets(self):
        secrets = []
        response = {}
        while True:
            try:
                if 'NextToken' in response:
                    response = self.secretsmanager_client.list_secrets(NextToken = response['NextToken'])
                else:
                    response = self.secretsmanager_client.list_secrets()

                secrets.extend(response['SecretList'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call SECRET_MANAGER list_secrets', {'region': self.region})

            if 'NextToken' not in response:
                break
        
        return secrets

    def secret_not_encrypted_with_kms_cmk(self):
        failures = []
        
        for secret in self.secretsmanager_secrets:
            if 'KmsKeyId' in secret:
                response = self.helper.get_kms_key_details(secret['KmsKeyId'])
                if response['KeyManager'] != 'CUSTOMER' :
                    failures = self.helper.append_item_to_list(failures, 'secretsmanager', secret['Name'], secret['ARN'], self.region)
        return failures
        
    def secret_rotation_not_enabled(self):
        failures = []
        
        for secret in self.secretsmanager_secrets:
            if 'RotationEnabled' in secret:
                if not secret['RotationEnabled']:
                    failures = self.helper.append_item_to_list(failures, 'secretsmanager', secret['Name'], secret['ARN'], self.region)

        return failures
        
    def secret_rotation_interval_not_configured(self):
        failures = []
        for secret in self.secretsmanager_secrets:            
            if 'RotationRules' in secret:
                if len(secret['RotationRules']): 
                    failures = self.helper.append_item_to_list(failures, 'secretsmanager', secret['Name'], secret['ARN'], self.region)
        
        return failures
    
    