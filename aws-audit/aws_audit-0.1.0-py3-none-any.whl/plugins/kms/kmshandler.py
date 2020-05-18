import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class kmshandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create KMS client
            self.kms_client = session.client('kms', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create KMS client', {'region': self.region})

        self.kms_keys = self.list_kms_keys()

    # List all kms keys and put it in kms_keys attribute
    def list_kms_keys(self):
        keys = []
        response = {}

        while True:

            try:
                if 'Truncated' in response:
                    if response['Truncated']:
                        response = self.kms_client.list_keys(Marker=response['NextMarker'])
                else:
                    response = self.kms_client.list_keys()
                
                keys.extend(response['Keys'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call KMS list_keys', {'region': self.region})

            if not response['Truncated']:
                break

        return keys
        
    # Get kms key policy
    def get_kms_key_policy(self, keyid):
        try:
            response = self.kms_client.get_key_policy(KeyId=keyid,PolicyName='default')

            return response['Policy']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call KMS get_key_policy for key : '+ keyid, {'region': self.region})
        
    # Get key rotation status
    def get_kms_key_rotation_status(self, keyid):
        try:
            response = self.kms_client.get_key_rotation_status(KeyId=keyid)

            return response['KeyRotationEnabled']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call KMS get_key_rotation_status for key : '+ keyid, {'region': self.region})
        
    # describe key
    def describe_kms_key(self, keyid):
        try:
            response = self.kms_client.describe_key(KeyId=keyid)

            return response['KeyMetadata']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call KMS describe_key for key : '+ keyid, {'region': self.region})

    def kms_key_exposed(self):
        failures = []

        for kms_key in  self.kms_keys:
            try:
                policy = self.get_kms_key_policy(kms_key['KeyId'])
                
                policy_statement = json.loads(policy)

                is_exposed = self.helper.is_policy_exposed_to_everyone(policy_statement)
                if is_exposed:
                    failures = self.helper.append_item_to_list(failures, 'kms', kms_key['KeyId'], kms_key['KeyArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting kms key policy - {kms_key['KeyArn']} : {e}")

        return failures

    def kms_key_rotation_not_enabled(self):
        failures = []
        for kms_key in self.kms_keys:
            
            try:
                key_details = self.describe_kms_key(kms_key['KeyId'])

            except Exception as e:
                self.logger.error(f"Error while getting kms key details - {kms_key['KeyArn']} : {e}")
            
            if key_details['KeyManager'] == "CUSTOMER":
                try:
                    key_rotation_status = self.get_kms_key_rotation_status(kms_key['KeyId'])
    
                except Exception as e:                
                    self.logger.error(f"Error while getting kms key rotation status - {kms_key['KeyArn']} : {e}")
    
                if not key_rotation_status:
                    failures = self.helper.append_item_to_list(failures, 'kms', kms_key['KeyId'], kms_key['KeyArn'] , self.region)

        return failures

    def kms_key_scheduled_for_deletion(self):
        failures = []

        for kms_key in self.kms_keys:
            try:
                key_details = self.describe_kms_key(kms_key['KeyId'])
                
            except Exception as e:
                self.logger.error(f"Error while getting kms key details - {kms_key['KeyArn']} : {e}")
                continue    

            if key_details['KeyState'] == 'PendingDeletion':
                failures = self.helper.append_item_to_list(failures, 'kms', kms_key['KeyId'], kms_key['KeyArn'] , self.region)

        return failures

    def kms_key_cross_account_access(self):
        failures = []

        for kms_key in  self.kms_keys:
            try:
                policy = self.get_kms_key_policy(kms_key['KeyId'])
                
                policy_statement = json.loads(policy)

                has_caa_enabled = self.helper.is_policy_has_cross_account_access(policy_statement)
                if has_caa_enabled:
                    failures = self.helper.append_item_to_list(failures, 'kms', kms_key['KeyId'], kms_key['KeyArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting kms key policy - {kms_key['KeyArn']} : {e}")
                continue
            
        return failures