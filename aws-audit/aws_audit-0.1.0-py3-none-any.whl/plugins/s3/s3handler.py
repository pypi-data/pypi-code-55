import json, os
from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class s3handler : 
    
    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create s3 client
            self.s3_client = session.client('s3', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create s3 client', {'region': self.region})
        
        
        self.buckets = self.list_buckets()
        self.buckets_policies = {}
        self.buckets_encryptions = {}
        
    def list_buckets(self):
        try:
            response = self.s3_client.list_buckets()

            return response['Buckets']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call s3 list_buckets', {'region': self.region})
    
    def get_bucket_policy(self, bucket_name):
        try:
            response = self.s3_client.get_bucket_policy(Bucket=bucket_name)
            self.buckets_policies[bucket_name] = response

            return response
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                self.buckets_policies[bucket_name] = 'NoSuchBucketPolicy'
                return 'NoSuchBucketPolicy'
            else:
                raise classify_error(self.logger, e, 'Failed to call S3 get_bucket_policy', {'region': self.region})        

    def get_object_lock_configuration(self, bucket_name):
        try:
            response = self.s3_client.get_object_lock_configuration(Bucket=bucket_name)

            return response

        except ClientError as e:
            if e.response['Error']['Code'] == 'ObjectLockConfigurationNotFoundError':
                return 'ObjectLockConfigurationNotFoundError'
            else:
                raise classify_error(self.logger, e, 'Failed to call S3 get_object_lock_configuration', {'region': self.region})
    
    def get_bucket_lifecycle_configuration(self, bucket_name):
        try:
            response = self.s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)

            return response

        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                return 'NoSuchLifecycleConfiguration'
            else:
                raise classify_error(self.logger, e, 'Failed to call S3 get_bucket_lifecycle_configuration', {'region': self.region})

    def get_bucket_encryption(self, bucket_name):
        try:
            response = self.s3_client.get_bucket_encryption(Bucket=bucket_name)
            self.buckets_encryptions[bucket_name] = response
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                self.buckets_encryptions[bucket_name] = 'ServerSideEncryptionConfigurationNotFoundError'
                return 'ServerSideEncryptionConfigurationNotFoundError'
            else:
                raise classify_error(self.logger, e, 'Failed to call S3 get_bucket_encryption', {'region': self.region})

    def get_bucket_acl(self, bucket):
        try:
            response = self.s3_client.get_bucket_acl(Bucket=bucket)

            return response['Grants']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call S3 get_bucket_acl', {'region': self.region})

    def s3_server_side_encryption_not_enabled(self):
        
        failures = []
        
        for bucket in self.buckets:
            try:
                if bucket['Name'] not in self.buckets_encryptions:
                    result = self.get_bucket_encryption(bucket['Name'])
                else:
                    result = self.buckets_encryptions[bucket['Name']]
                if not isinstance(result, dict):
                    failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region)
                    
            except Exception as e:
                self.logger.error(f"Error while getting S3 encryption details - {bucket['Name']} : {e}")
                continue
        
        return failures
    
    def s3_bucket_intransit_encyption_not_enabled(self):
        failures = []

        for bucket in self.buckets:
            try:
                if bucket['Name'] not in self.buckets_policies:
                    result = self.get_bucket_policy(bucket['Name'])
                else:
                    result = self.buckets_policies[bucket['Name']]
                
                if isinstance(result, dict):
                    policy = json.loads(result['Policy'])
                    is_configured = 0
                    for statement in policy['Statement']:
                        if statement['Effect'] == "Allow" and 'Condition' in statement:
                            if 'Bool' in statement['Condition']:
                                if 'aws:SecureTransport' in statement['Condition']['Bool']:
                                    if statement['Condition']['Bool']['aws:SecureTransport'] == 'true':
                                        is_configured = 1
                        elif statement['Effect'] == "Deny" and 'Condition' in statement:
                            if 'Bool' in statement['Condition']:
                                if 'aws:SecureTransport' in statement['Condition']['Bool']:
                                    if statement['Condition']['Bool']['aws:SecureTransport'] == 'false':
                                        is_configured = 1

                    if not is_configured:
                        failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region)
                    
                else:
                    msg = "Bucket policy not defined."
                    failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region, msg)

            except Exception as e:
                self.logger.error(f"Error while getting S3 policy details - {bucket['Name']} : {e}")
                continue

        return failures

    def s3_bucket_object_lock_not_enabled(self):
        failures = []

        for bucket in self.buckets:
            try:
                result = self.get_object_lock_configuration(bucket['Name'])
                if isinstance(result, dict):
                    if result['ObjectLockConfiguration']['ObjectLockEnabled'] != 'Enabled':
                        failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region)
                else:
                    failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting S3 object lock configuration details - {bucket['Name']} : {e}")
                continue
        
        return failures

    def s3_bucket_cross_account_access_allowed(self):
        failures = []

        for bucket in self.buckets:
            try:
                result = self.get_bucket_policy(bucket['Name'])
                if isinstance(result, dict):
                    policy = json.loads(result['Policy'])
                    is_caa_enabled  = self.helper.is_policy_has_cross_account_access(policy)
                    if is_caa_enabled:
                        failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting S3 policy details - {bucket['Name']} : {e}")
                continue

        return failures

    def s3_bucket_lifecycle_rules_not_configured(self):
        failures = []

        for bucket in self.buckets:
            try:
                result = self.get_bucket_lifecycle_configuration(bucket['Name'])
                if not isinstance(result, dict):
                    failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region)
            except Exception as e:
                self.logger.error(f"Error while getting S3 lifecycle configuration details - {bucket['Name']} : {e}")
                continue

        return failures
    
    def s3_bucket_not_encypted_with_kms_cmk(self):
        failures = []

        for bucket in self.buckets:
            try:
                if bucket['Name'] in self.buckets_encryptions:
                    result = self.buckets_encryptions[bucket['Name']]
                else:
                    result = self.get_bucket_encryption(bucket['Name'])

                if not isinstance(result, dict):
                    failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region)
                else:
                    for rules in result['ServerSideEncryptionConfiguration']['Rules']:
                        if 'KMSMasterKeyID' in rules['ApplyServerSideEncryptionByDefault']:
                            KMSMasterKeyID = rules['ApplyServerSideEncryptionByDefault']['KMSMasterKeyID']
                            response = self.helper.get_kms_key_details(KMSMasterKeyID)
                            if response['KeyManager'] != 'CUSTOMER' : 
                                failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region)
                                break

            except Exception as e:
                self.logger.error(f"Error while getting S3 encryption details - {bucket['Name']} : {e}")
                continue

        return failures

    def s3_bucket_default_encyption_not_enabled(self):
        failures = []

        for bucket in self.buckets:
            try:
                if bucket['Name'] in self.buckets_encryptions:
                    result = self.buckets_encryptions[bucket['Name']]
                else:
                    result = self.get_bucket_encryption(bucket['Name'])
                
                if not isinstance(result, dict):
                    failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region)
                    
            except Exception as e:
                self.logger.error(f"Error while getting S3 encryption details - {bucket['Name']} : {e}")
                continue

        return failures

    def s3_bucket_allow_global_acl_permissions(self):
        failures = []

        for bucket in self.buckets:
            try:
                result = self.get_bucket_acl(bucket['Name'])
                for grant in result:
                    if 'URI' in grant['Grantee']:
                        if grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                            msg = f"ACL Grantee AllUsers allowed permission: { grant['Permission'] }"
                            failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region, msg)
                        if grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers':
                            msg = f"ACL Grantee AuthenticatedUsers allowed permission: { grant['Permission'] }"
                            failures = self.helper.append_item_to_list(failures, 's3', bucket['Name'], bucket['Name'], self.region, msg)
            except Exception as e:
                self.logger.error(f"Error while getting S3 bucket acl details - {bucket['Name']} : {e}")
        
        return failures