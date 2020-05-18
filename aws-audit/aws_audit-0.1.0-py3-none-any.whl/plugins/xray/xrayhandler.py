import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class xrayhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create X-Ray client
            self.xray_client = session.client('xray', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create X-Ray client', {'region': self.region})
    
    def xray_not_encrypted_with_kms_cmk(self):
        failures = []
        try:
            xray_encryption = self.xray_client.get_encryption_config()
            if xray_encryption['EncryptionConfig']['Type'] == 'NONE':
                msg = "Default encryption in use for xray."
                failures = self.helper.append_item_to_list(failures, 'xray', "", "", self.region, msg)
            elif xray_encryption['EncryptionConfig']['Type'] == 'KMS':
                key_id = xray_encryption['EncryptionConfig']['KeyId'].split('/')
                key_details = self.helper.get_kms_key_details(key_id[1])
                if key_details['KeyManager'] != 'CUSTOMER':
                    msg = "AWS Managed KMS Key 'aws/xray' is in use for xray encryption."
                    failures = self.helper.append_item_to_list(failures, 'xray', "", "", self.region, msg)

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call X-Ray get_encryption_config', {'region': self.region})

        return failures