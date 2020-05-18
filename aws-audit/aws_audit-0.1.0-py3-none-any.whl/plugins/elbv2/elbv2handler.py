import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class elbv2handler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        self.badCipers = [
            'Protocol-SSLv2',
            'Protocol-SSLv3',
            'DHE-RSA-AES128-SHA',
            'DHE-DSS-AES128-SHA',
            'CAMELLIA128-SHA',
            'EDH-RSA-DES-CBC3-SHA',
            'ECDHE-RSA-RC4-SHA',
            'RC4-SHA',
            'ECDHE-ECDSA-RC4-SHA',
            'DHE-DSS-AES256-GCM-SHA384',
            'DHE-RSA-AES256-GCM-SHA384',
            'DHE-RSA-AES256-SHA256',
            'DHE-DSS-AES256-SHA256',
            'DHE-RSA-AES256-SHA',
            'DHE-DSS-AES256-SHA',
            'DHE-RSA-CAMELLIA256-SHA',
            'DHE-DSS-CAMELLIA256-SHA',
            'CAMELLIA256-SHA',
            'EDH-DSS-DES-CBC3-SHA',
            'DHE-DSS-AES128-GCM-SHA256',
            'DHE-RSA-AES128-GCM-SHA256',
            'DHE-RSA-AES128-SHA256',
            'DHE-DSS-AES128-SHA256',
            'DHE-RSA-CAMELLIA128-SHA',
            'DHE-DSS-CAMELLIA128-SHA',
            'ADH-AES128-GCM-SHA256',
            'ADH-AES128-SHA',
            'ADH-AES128-SHA256',
            'ADH-AES256-GCM-SHA384',
            'ADH-AES256-SHA',
            'ADH-AES256-SHA256',
            'ADH-CAMELLIA128-SHA',
            'ADH-CAMELLIA256-SHA',
            'ADH-DES-CBC3-SHA',
            'ADH-DES-CBC-SHA',
            'ADH-RC4-MD5',
            'ADH-SEED-SHA',
            'DES-CBC-SHA',
            'DHE-DSS-SEED-SHA',
            'DHE-RSA-SEED-SHA',
            'EDH-DSS-DES-CBC-SHA',
            'EDH-RSA-DES-CBC-SHA',
            'IDEA-CBC-SHA',
            'RC4-MD5',
            'SEED-SHA',
            'DES-CBC3-MD5',
            'DES-CBC-MD5',
            'RC2-CBC-MD5',
            'PSK-AES256-CBC-SHA',
            'PSK-3DES-EDE-CBC-SHA',
            'KRB5-DES-CBC3-SHA',
            'KRB5-DES-CBC3-MD5',
            'PSK-AES128-CBC-SHA',
            'PSK-RC4-SHA',
            'KRB5-RC4-SHA',
            'KRB5-RC4-MD5',
            'KRB5-DES-CBC-SHA',
            'KRB5-DES-CBC-MD5',
            'EXP-EDH-RSA-DES-CBC-SHA',
            'EXP-EDH-DSS-DES-CBC-SHA',
            'EXP-ADH-DES-CBC-SHA',
            'EXP-DES-CBC-SHA',
            'EXP-RC2-CBC-MD5',
            'EXP-KRB5-RC2-CBC-SHA',
            'EXP-KRB5-DES-CBC-SHA',
            'EXP-KRB5-RC2-CBC-MD5',
            'EXP-KRB5-DES-CBC-MD5',
            'EXP-ADH-RC4-MD5',
            'EXP-RC4-MD5',
            'EXP-KRB5-RC4-SHA',
            'EXP-KRB5-RC4-MD5'
        ]

        try:
            # Create elbv2 client
            self.elb_client = session.client('elbv2', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create elbv2 client', {'region': self.region})

        try:
            # Create wafv2 client
            self.waf_client = session.client('wafv2', region_name=region)
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create wafv2 client', {'region': self.region})

        self.elbs = self.describe_load_balancers()

    # List all kms keys and put it in kms_keys attribute
    def describe_load_balancers(self):
        elbs = []
        response = {}

        while True:

            try:
                if 'NextMarker' in response:
                    response = self.elb_client.describe_load_balancers(Marker = response['NextMarker'])
                else:
                    response = self.elb_client.describe_load_balancers()

                elbs.extend(response['LoadBalancers'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call ELB describe_load_balancers', {'region': self.region})

            if 'NextMarker' not in response:
                break

        return elbs
        
    # Describe listeners for elb
    def describe_listeners(self, elb_arn):
        listeners = []
        response = {}

        while True:

            try:
                if 'NextMarker' in response:
                    response = self.elb_client.describe_listeners(LoadBalancerArn=elb_arn, Marker=response['NextMarker'])
                else:
                    response = self.elb_client.describe_listeners(LoadBalancerArn=elb_arn)

                listeners.extend(response['Listeners'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call ELB describe_listeners', {'region': self.region})

            if 'NextMarker' not in response:
                break

        return listeners
        
    # describe load balancer attributes
    def describe_load_balancer_attributes(self, elb_arn):
        try:
            reponse = self.elb_client.describe_load_balancer_attributes(LoadBalancerArn=elb_arn)

            return reponse['Attributes']
        
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call ELB describe_load_balancer_attributes', {'region': self.region})
        
    # get ssl policy details for keys (Ciphers, SslProtocols) 
    def get_ssl_policy_details(self, ssl_policy, key):
        
        result = []
        
        try:
            response = self.elb_client.describe_ssl_policies(Names=[ssl_policy])
            
            if key == 'Ciphers':
                ciphers_list = response['SslPolicies'][0]['Ciphers']
                for cipher in ciphers_list:
                    result.append(cipher['Name'])
            elif key == 'SslProtocols' : 
                result = response['SslPolicies'][0]['SslProtocols']
        
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call ELB get_ssl_policy_details', {'region': self.region})
            
        return result
        
    # Get list of all waf web acls
    def list_web_acls(self):
        webacls = []
        response = {}

        while True:

            try:
                if 'NextMarker' in response:
                    response = self.waf_client.list_web_acls(Scope='REGIONAL',NextMarker=response['NextMarker'])
                else:
                    response = self.waf_client.list_web_acls(Scope='REGIONAL')

                webacls.extend(response['WebACLs'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call ELB list_web_acls', {'region': self.region})

            if 'NextMarker' not in response:
                break

        return webacls

    # List resources for web acls
    def list_resources_for_web_acl(self,webacl):
        try:
            response = self.waf_client.list_resources_for_web_acl(WebACLArn=webacl,ResourceType='APPLICATION_LOAD_BALANCER')

            return response['ResourceArns']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call WAF list_resources_for_web_acl', {'region': self.region})

    # check elb has enabled https listener only
    def elb_not_using_https_listener(self):
        failures = []
        for elb in self.elbs:
            try:
                listeners = self.describe_listeners(elb['LoadBalancerArn'])
                if elb['Type'] == 'application' : 
                    non_https_listner = []
                    for listener in listeners:
                        if listener['Protocol'] != 'HTTPS':
                            non_https_listner.append(listener['ListenerArn'])
                    
                    if len(non_https_listner) > 0:
                        msg = "%s load balancer has non https listeners. : %s" %(elb['LoadBalancerName'],', '.join(non_https_listner))
                        failures = self.helper.append_item_to_list(failures, 'elbv2', elb['LoadBalancerName'], elb['LoadBalancerArn'] , self.region, msg)

                elif elb['Type'] == 'network' : 
                    non_tls_listner = []
                    for listener in listeners:
                        if listener['Protocol'] != 'TLS':
                            non_tls_listner.append(listener['ListenerArn'])
                    
                    if len(non_tls_listner) > 0:
                        msg = "%s load balancer has non tls listeners. : %s" %(elb['LoadBalancerName'],', '.join(non_tls_listner))
                        failures = self.helper.append_item_to_list(failures, 'elbv2', elb['LoadBalancerName'], elb['LoadBalancerArn'] , self.region, msg)
            
            except Exception as e:
                self.logger.error(f"Error while getting load balancer listener details : {e}")

        return failures

    # Check logging is enabled or not
    def elb_logging_not_enabled(self):
        failures = []
        for elb in self.elbs:
            try:
                elb_attributes = self.describe_load_balancer_attributes(elb['LoadBalancerArn'])
                for attribute in elb_attributes:
                    if attribute['Key'] == 'access_logs.s3.enabled' and attribute['Value'] != 'true':
                        failures = self.helper.append_item_to_list(failures, 'elbv2', elb['LoadBalancerName'], elb['LoadBalancerArn'] , self.region)
            except Exception as e:
                self.logger.error(f"Error while getting load balancer attribute details- {elb['LoadBalancerArn']} : {e}")

        return failures

    # Check waf is enabled for alb
    def elb_waf_not_enabled(self):
        failures = []
        
        """ Build list of all load balancer"""
        laodbalancers = []
        for elb in self.elbs:
            laodbalancers.append(elb['LoadBalancerArn'])
        
        """ Get all webacls"""
        webacls = []
        try:
            webacls = self.list_web_acls()
        except Exception as e:
            self.logger.error(f"Error while getting list of webacls : {e}")
            
        all_resources = []

        for webacl in webacls:
            """ Get resources for webacls and check load balancer arn in it or not """
            try:
                resources = self.list_resources_for_web_acl(webacl)
                all_resources.append(resources)
            
            except Exception as e:                
                self.logger.error(f"Error while fetching resources for web acls- {webacl} : {e}")                
                
        for laodbalancer in laodbalancers:
            if laodbalancer not in all_resources:
                failures = self.helper.append_item_to_list(failures, 'elbv2', laodbalancer, laodbalancer, self.region)

        return failures

    # Check elb using insecure ciphers
    def elb_using_insecure_ciphers(self):
        failures = []
        for elb in self.elbs:
            try:
                listeners = self.describe_listeners(elb['LoadBalancerArn'])
                elb_bad_ciphers = []
                for listener in listeners:
                    if 'SslPolicy' in listener:
                        ssl_ciphers = self.get_ssl_policy_details(listener['SslPolicy'],'Ciphers')
                        for cipher in ssl_ciphers:
                            if cipher in self.badCipers:
                                elb_bad_ciphers.append(cipher)
                
                if len(elb_bad_ciphers) > 0 :
                    msg = "%s load balancer using insecure ciphers : %s" %(elb['LoadBalancerName'],', '.join(elb_bad_ciphers))
                    failures = self.helper.append_item_to_list(failures, 'elbv2', elb['LoadBalancerName'], elb['LoadBalancerArn'] , self.region, msg)

            except Exception as e:
                self.logger.error(f"Error while getting load balancer listener details- {elb['LoadBalancerArn']} : {e}")

        return failures
        
    def elb_invalid_http_header_dropped_not_enabled(self):
        failures = []
        for elb in self.elbs:
            try:
                elb_attributes = self.describe_load_balancer_attributes(elb['LoadBalancerArn'])
                for attribute in elb_attributes:
                    if attribute['Key'] == 'routing.http.drop_invalid_header_fields.enabled' and attribute['Value'] != 'true':
                        failures = self.helper.append_item_to_list(failures, 'elbv2', elb['LoadBalancerName'], elb['LoadBalancerArn'] , self.region)
            except Exception as e:
                self.logger.error(f"Error while getting load balancer attribute details- {elb['LoadBalancerArn']} : {e}")

        return failures

    def elb_deletion_protection_not_enabled(self):
        failures = []
        for elb in self.elbs:
            try:
                elb_attributes = self.describe_load_balancer_attributes(elb['LoadBalancerArn'])
                for attribute in elb_attributes:
                    if attribute['Key'] == 'deletion_protection.enabled' and attribute['Value'] != 'true':
                        failures = self.helper.append_item_to_list(failures, 'elbv2', elb['LoadBalancerName'], elb['LoadBalancerArn'] , self.region)
            except Exception as e:
                self.logger.error(f"Error while getting load balancer attribute details- {elb['LoadBalancerArn']} : {e}")

        return failures

    