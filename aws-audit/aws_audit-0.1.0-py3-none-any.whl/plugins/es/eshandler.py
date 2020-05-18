import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class eshandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create ElasticSearch client
            self.es_client = session.client('es', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create ElasticSearch client', {'region': self.region})

        self.domain_names = self.list_domain_names()

    def list_domain_names(self):
        domain_names = []
        try:

            response = self.es_client.list_domain_names()

            for domain in response['DomainNames']:
                domain_names.append(domain['DomainName'])

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call ElasticSearch list_domain_names', {'region': self.region})
        
        return domain_names

    def describe_elasticsearch_domain(self, domain_name):
        try:

            response = self.es_client.describe_elasticsearch_domain(DomainName=domain_name)

            return response['DomainStatus']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call ElasticSearch describe_elasticsearch_domain', {'region': self.region})

    def es_domain_not_encypted_kms_cmk(self):

        failures = []

        for domain_name in self.domain_names:
            try:
                response = self.describe_elasticsearch_domain(domain_name)

                if response['EncryptionAtRestOptions']['Enabled']:
                    kms = self.helper.get_kms_key_details( response['EncryptionAtRestOptions']['KmsKeyId'] )
                    if kms['KeyManager'] != 'CUSTOMER' :
                        failures = self.helper.append_item_to_list(failures, 'es', response['DomainName'], response['ARN'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting ElasticSearch domain details - { domain_name }: {e}")
                continue
        
        return failures

    def es_node_to_node_encyption_not_enabled(self):
        failures = []

        for domain_name in self.domain_names:
            try:
                response = self.describe_elasticsearch_domain(domain_name)

                if not response['NodeToNodeEncryptionOptions']['Enabled']:                    
                    failures = self.helper.append_item_to_list(failures, 'es', response['DomainName'], response['ARN'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting ElasticSearch domain details - { domain_name }: {e}")
                continue
        
        return failures

    def es_domain_exposed_to_everyone(self):
        failures = []

        for domain_name in self.domain_names:
            try:
                response = self.describe_elasticsearch_domain(domain_name)
                policy_statements = json.loads(response['AccessPolicies'])
                is_exposed = self.helper.is_policy_exposed_to_everyone(policy_statements)
                if is_exposed:
                    failures = self.helper.append_item_to_list(failures, 'es', response['DomainName'], response['ARN'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting ElasticSearch domain details - { domain_name }: {e}")
                continue
        
        return failures

    def es_allow_cross_account_access(self):
        failures = []

        for domain_name in self.domain_names:
            try:
                response = self.describe_elasticsearch_domain(domain_name)
                policy_statements = json.loads(response['AccessPolicies'])
                is_caa_enabled = self.helper.is_policy_has_cross_account_access(policy_statements)
                if is_caa_enabled:
                    failures = self.helper.append_item_to_list(failures, 'es', response['DomainName'], response['ARN'] , self.region)
     
            except Exception as e:
                self.logger.error(f"Error while getting ElasticSearch domain details - { domain_name }: {e}")
                continue
        
        return failures

    def es_domain_not_in_vpc(self):
        failures = []

        for domain_name in self.domain_names:
            try:
                response = self.describe_elasticsearch_domain(domain_name)

                if 'VPCOptions' not in response:                    
                    failures = self.helper.append_item_to_list(failures, 'es', response['DomainName'], response['ARN'] , self.region)
                
            except Exception as e:
                self.logger.error(f"Error while getting ElasticSearch domain details - { domain_name }: {e}")
                continue
        
        return failures

    def es_domain_encyption_at_rest_not_enabled(self):
        failures = []

        for domain_name in self.domain_names:
            try:
                response = self.describe_elasticsearch_domain(domain_name)

                if not response['EncryptionAtRestOptions']['Enabled']:
                    failures = self.helper.append_item_to_list(failures, 'es', response['DomainName'], response['ARN'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting ElasticSearch domain details - { domain_name }: {e}")
                continue
        
        return failures
    
    def es_domain_not_enforcing_https_connections(self):
        failures = []

        for domain_name in self.domain_names:
            try:
                response = self.describe_elasticsearch_domain(domain_name)

                if not response['DomainEndpointOptions']['EnforceHTTPS']:
                    failures = self.helper.append_item_to_list(failures, 'es', response['DomainName'], response['ARN'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting ElasticSearch domain details - { domain_name }: {e}")
                continue
        
        return failures