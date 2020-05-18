import json, os
# from botocore.exceptions import Exception
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class cloudtrailhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create cloudtrail client
            self.cloudtrail_client = session.client('cloudtrail', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create cloudtrail client', {'region': self.region})

        try:
            # Create S3 client
            self.s3_client = session.client('s3', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create S3 client', {'region': self.region})
        
        self.trails = self.describe_trails()

    def describe_trails(self):
        trails = []
        try:
            response = self.cloudtrail_client.describe_trails()

            if response['trailList']:
                trails.extend(response['trailList'])

            return trails
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call cloudtrail describe_trails', {'region': self.region})

    def get_event_selectors(self, trail_name):
        try:
            response = self.cloudtrail_client.get_event_selectors(TrailName=trail_name)

            return response

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call cloudtrail describe_trails', {'region': self.region})

    def get_trail_status(self, trail_name):
        try:
            response = self.cloudtrail_client.get_trail_status(Name=trail_name)

            return response

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call cloudtrail describe_trails', {'region': self.region})

    def get_bucket_logging(self, bucket):
        try:
            response = self.s3_client.get_bucket_logging(Bucket=bucket)

            return response

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call S3 get_bucket_logging', {'region': self.region})

    def get_bucket_acl(self, bucket):
        try:
            response = self.s3_client.get_bucket_acl(Bucket=bucket)

            return response['Grants']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call S3 get_bucket_acl', {'region': self.region})

    def cloudtrail_not_enabled(self):
        failures = []
        if not self.trails:
            msg = f"Cloudtrail is not enabled for {self.region}"
            failures = self.helper.append_item_to_list(failures, 'cloudtrail', "", "", self.region, msg)

        return failures

    def cloudtrail_global_services_not_enabled(self):
        failures = []

        for trail in self.trails:
            if not trail['IncludeGlobalServiceEvents']:
                failures = self.helper.append_item_to_list(failures, 'cloudtrail', trail['Name'], trail['TrailARN'] , self.region)

        return failures

    def cloudtrail_logs_not_encrypted(self):
        failures = []

        for trail in self.trails:
            if 'KmsKeyId' not in trail:
                failures = self.helper.append_item_to_list(failures, 'cloudtrail', trail['Name'], trail['TrailARN'] , self.region)

        return failures

    def cloudtrail_management_event_not_included(self):
        failures = []
        for trail in self.trails:
            result = self.get_event_selectors(trail['Name'])
            failed = 0
            if 'EventSelectors' in result:
                for eventselector in result['EventSelectors']:
                    if not eventselector['IncludeManagementEvents']:
                        failed = 1
                        break
            if failed:
                failures = self.helper.append_item_to_list(failures, 'cloudtrail', trail['Name'], trail['TrailARN'] , self.region)

        return failures

    def cloudtrail_log_file_integrity_validation_enabled(self):
        failures = []

        for trail in self.trails:
            if not trail['LogFileValidationEnabled']:
                failures = self.helper.append_item_to_list(failures, 'cloudtrail', trail['Name'], trail['TrailARN'] , self.region)

        return failures

    def cloudtrail_log_delivery_failing(self):
        failures = []
        for trail in self.trails:
            result = self.get_trail_status(trail['Name'])
            if 'LatestDeliveryError' in result:
                if not result['LatestDeliveryError']:
                    failures = self.helper.append_item_to_list(failures, 'cloudtrail', trail['Name'], trail['TrailARN'] , self.region)

        return failures

    def cloudtrail_bucket_logging_not_enabled(self):
        failures = []

        for trail in self.trails:
            try:
                response = self.get_bucket_logging(trail['S3BucketName'])

                if 'LoggingEnabled' not in response:
                    failures = self.helper.append_item_to_list(failures, 'cloudtrail', trail['Name'], trail['TrailARN'] , self.region)
            
            except Exception  as e:
                self.logger.error(f"Error while getting S3 bucket logging details: {e}")

        return failures

    def cloudtrail_bucket_is_public(self):
        failures = []

        for trail in self.trails:
            try:
                response = self.get_bucket_acl(trail['S3BucketName'])

                for grant in response:
                    permission = ['FULL_CONTROL', 'WRITE', 'WRITE_ACP', 'READ', 'READ_ACP']
                    if 'URI' in grant['Grantee']:
                        if grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers' and grant['Permission'] in permission:
                            failures = self.helper.append_item_to_list(failures, 'cloudtrail', trail['Name'], trail['TrailARN'] , self.region)

            except Exception  as e:
                self.logger.error(f"Error while getting S3 bucket logging details: {e}")
            
        return failures
