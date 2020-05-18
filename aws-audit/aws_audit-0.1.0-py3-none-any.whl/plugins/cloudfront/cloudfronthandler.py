import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class cloudfronthandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Cloudfront client
            self.cloudfront_client = session.client('cloudfront', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Cloudfront client', {'region': self.region})

        self.distributions = self.list_distributions()
    
    def list_distributions(self):
        distributions = []
        response = {}

        while True:

            try:
                if 'DistributionList' in response:
                    if 'NextMarker' in response['DistributionList']:
                        response = self.cloudfront_client.list_distributions(Marker = response['DistributionList']['NextMarker'])
                else:
                    response = self.cloudfront_client.list_distributions()

                if 'Items' in response['DistributionList']:
                    distributions.extend(response['DistributionList']['Items'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Cloudfront list_distributions', {'region': self.region})

            if 'NextMarker' not in response['DistributionList']:
                break

        return distributions

    def get_distribution_config(self, distribution_id):
        try:
            response = self.cloudfront_client.get_distribution_config(Id=distribution_id)

            return response['DistributionConfig']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call Cloudfront list_distributions', {'region': self.region})

    def cloudfront_geo_restriction_not_enabled(self):
        failures = []

        for distribution in self.distributions:
            if distribution['Restrictions']['GeoRestriction']['RestrictionType'] == 'none':
                failures = self.helper.append_item_to_list(failures, 'cloudfront', distribution['Id'], distribution['ARN'] , self.region)

        return failures

    def cloudfront_using_insecure_origin_ssl_protocols(self):
        failures = []

        for distribution in self.distributions:
            for item in distribution['Origins']['Items']:
                if 'CustomOriginConfig' in item:
                    if 'SSLv3' in item['CustomOriginConfig']['OriginSslProtocols']['Items']:
                        failures = self.helper.append_item_to_list(failures, 'cloudfront', distribution['Id'], distribution['ARN'] , self.region)

        return failures

    def cloudfront_not_integrated_with_waf(self):
        failures = []

        for distribution in self.distributions:
            if distribution['WebACLId'] == "":
                failures = self.helper.append_item_to_list(failures, 'cloudfront', distribution['Id'], distribution['ARN'] , self.region)

        return failures

    def cloudfront_access_logging_not_enabled(self):
        failures = []

        for distribution in self.distributions:
            try:
                config = self.get_distribution_config(distribution['Id'])
                if not config['Logging']['Enabled']:
                    failures = self.helper.append_item_to_list(failures, 'cloudfront', distribution['Id'], distribution['ARN'] , self.region)
            except Exception as e:
                self.logger.error(f"Error while getting distribution config details: {e}")            

        return failures

    def cloudfront_not_using_improved_security_policy_for_https(self):
        failures = []

        for distribution in self.distributions:
            if distribution['ViewerCertificate']['MinimumProtocolVersion'] in ['TLSv1', 'TLSv1_2016']:
                failures = self.helper.append_item_to_list(failures, 'cloudfront', distribution['Id'], distribution['ARN'] , self.region)

        return failures

    def cloudfront_traffic_to_origin_unencrypted(self):
        failures = []

        for distribution in self.distributions:
            for item in distribution['Origins']['Items']:
                if 'CustomOriginConfig' in item:
                    if item['CustomOriginConfig']['OriginProtocolPolicy'] in  ['http-only', 'match-viewer'] :
                        failures = self.helper.append_item_to_list(failures, 'cloudfront', distribution['Id'], distribution['ARN'] , self.region)

        return failures

    def cloudfront_not_using_secure_protocol(self):
        failures = []

        for distribution in self.distributions:
            if distribution['DefaultCacheBehavior']['ViewerProtocolPolicy'] == 'allow-all' :
                failures = self.helper.append_item_to_list(failures, 'cloudfront', distribution['Id'], distribution['ARN'] , self.region)

        return failures

    def cloudfront_access_origin_identity_enabled(self):
        failures = []

        for distribution in self.distributions:
            for item in distribution['Origins']['Items']:
                if 'S3OriginConfig' in item:
                    if item['S3OriginConfig']['OriginAccessIdentity'] == "" :
                        failures = self.helper.append_item_to_list(failures, 'cloudfront', distribution['Id'], distribution['ARN'] , self.region)

        return failures

    def cloudfront_field_level_encryption_not_enabled(self):
        failures = []

        for distribution in self.distributions:
            if distribution['DefaultCacheBehavior']['FieldLevelEncryptionId'] == "" :
                failures = self.helper.append_item_to_list(failures, 'cloudfront', distribution['Id'], distribution['ARN'] , self.region)

        return failures