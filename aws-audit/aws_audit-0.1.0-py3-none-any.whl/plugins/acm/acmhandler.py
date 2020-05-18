import json, os
# from botocore.exceptions import Exception
# import boto3
# from boto3.session import Session
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error
from datetime import datetime, timedelta
from pytz import timezone
import pytz

class acmhandler : 
    
    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create ACM client
            self.acm_client = session.client('acm', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create ACM client', {'region': self.region})        
        
        self.acm_certificates = self.list_certificates()
        
    def list_certificates(self):
        acm_certificates = []
        response = {}

        while True:

            try:
                if 'NextToken' in response:
                    response = self.acm_client.list_certificates(NextToken = response['NextToken'])
                else:
                    response = self.acm_client.list_certificates()

                acm_certificates.extend(response['CertificateSummaryList'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call ACM list_certificates', {'region': self.region})

            if 'NextToken' not in response:
                break

        return acm_certificates
    
    def describe_certificate(self, certificate_arn):
        try:
            response = self.acm_client.describe_certificate(CertificateArn=certificate_arn)

            return response['Certificate']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call ACM list_certificates', {'region': self.region})
    
    def expired_certificates(self):
        
        failures = []
        
        for certificate in self.acm_certificates:
            try:
                result = self.describe_certificate(certificate['CertificateArn'])
                if result['Status'] == 'EXPIRED':
                    failures = self.helper.append_item_to_list(failures, 'acm', certificate['DomainName'], certificate['CertificateArn'], self.region)
                    
            except Exception as e:
                self.logger.error(f"Error while getting acm certificate details - {certificate['CertificateArn']} : {e}")
                continue
        
        return failures
        
    def certificates_with_wildcard_domain(self):
        failures = []
        
        for certificate in self.acm_certificates:
            try:
                failed = 0
                result = self.describe_certificate(certificate['CertificateArn'])
                
                if 'SubjectAlternativeNames' in result:
                    for alternate_name in result['SubjectAlternativeNames']:
                        if '*.' in alternate_name:
                            failed = 1
                
                if '*.' in certificate['DomainName']:
                    failed = 1

                if failed:
                    failures = self.helper.append_item_to_list(failures, 'acm', certificate['DomainName'], certificate['CertificateArn'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting acm certificate details - {certificate['CertificateArn']} : {e}")
                continue
            
        return failures
        
    def certificates_expires_in_30_days(self):
        failures = []
        utc=pytz.UTC
        for certificate in self.acm_certificates:
            try:
                result = self.describe_certificate(certificate['CertificateArn'])
                
                if 'NotAfter' in result:
                    renewal_date_timestamp = result['NotAfter']
                    renewal_date_timestamp = renewal_date_timestamp.replace(tzinfo=utc)
                    date_after_30_days = datetime.today() + timedelta(days=30)
                    date_after_30_days = date_after_30_days.replace(microsecond=0, tzinfo=utc)
                    if date_after_30_days > renewal_date_timestamp : 
                        failures = self.helper.append_item_to_list(failures, 'acm', certificate['DomainName'], certificate['CertificateArn'], self.region)
                    
            except Exception as e:
                self.logger.error(f"Error while getting acm certificate details - {certificate['CertificateArn']} : {e}")
                continue
            
        return failures
    
    