import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class route53handler : 
    
    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create route53domains client
            self.route53domains_client = session.client('route53domains', region_name=region)           
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create route53domains client', {'region': self.region})
        
        try:
            # Create route53 client
            self.route53_client = session.client('route53', region_name=region)

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create route53 client', {'region': self.region})    
        
        self.route53domains_domains = self.list_domains()
        self.route53_hosted_zones = self.list_hosted_zones()
        
    def list_domains(self):
        domains = []
        response = {}
        while True:
            try:
                if 'NextPageMarker' in response:
                    response = self.route53domains_client.list_domains(Marker = response['NextPageMarker'])
                else:
                    response = self.route53domains_client.list_domains()

                domains.extend(response['Domains'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call route53domains list_domains', {'region': self.region})

            if 'NextPageMarker' not in response:
                break

        return domains
    
    def list_hosted_zones(self):
        hosted_zones = []
        response = {}
        while True:
            try:
                if 'Marker' in response:
                    response = self.route53_client.list_hosted_zones(Marker = response['Marker'])
                else:
                    response = self.route53_client.list_hosted_zones()

                hosted_zones.extend(response['HostedZones'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call route53domains list_domains', {'region': self.region})

            if 'Marker' not in response:
                break
        
        return hosted_zones

    def list_resource_record_sets(self, id, domain_name, record_type):
        try:
            response = self.route53_client.list_resource_record_sets(HostedZoneId=id, StartRecordName=domain_name, StartRecordType=record_type)

            return response

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call route53 list_resource_record_sets', {'region': self.region})

    def get_domain_detail(self, domain_name):
        try:
            response = self.route53domains_client.get_domain_detail(DomainName=domain_name)

            return response

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call route53domains get_domain_detail', {'region': self.region})
    
    def route53domain_privacy_protection_not_enabled(self):
        failures = []
        for domain in self.route53domains_domains:
            try:
                result = self.get_domain_detail(domain['DomainName'])
                if 'RegistrantPrivacy' in result and not result['RegistrantPrivacy']:
                    failures = self.helper.append_item_to_list(failures, 'route53', domain['DomainName'], '-', self.region)
            except Exception as e:
                self.logger.error(f"Error while getting domain details - {domain['DomainName']} : {e}")
                continue
    
        return failures
        
    def route53_spf_record_not_present(self):
        failures = []
        for hosted_zone in self.route53_hosted_zones:
            try:
                id = hosted_zone['Id'].split('/')
                result = self.list_resource_record_sets(id[2], hosted_zone['Name'], 'SPF')
                record_sets = set([record['Type'] for record in result['ResourceRecordSets']])
                if 'SPF' not in record_sets:
                    failures = self.helper.append_item_to_list(failures, 'route53', hosted_zone['Name'], '-', self.region)
            except Exception as e:
                self.logger.error(f"Error while getting DNS record sets - {hosted_zone['Name']} : {e}")
                continue
        return failures
        
    def route53domain_transfter_lock_not_enabled(self):
        failures = []
        for domain in self.route53domains_domains:
            try:
                result = self.get_domain_detail(domain['DomainName'])
                if 'StatusList' in result and 'clientTransferProhibited' not in result['StatusList']:
                    failures = self.helper.append_item_to_list(failures, 'route53', domain['DomainName'], '-', self.region)
            except Exception as e:
                self.logger.error(f"Error while getting domain details - {domain['DomainName']} : {e}")
                continue

        return failures
    
    