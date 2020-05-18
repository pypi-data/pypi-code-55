import json, os
# import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
from aws_audit.utils.errors import classify_error

class CommonHelper:
    
    def __init__(self, session, region, logger):
        
        
        self.region = region
        self.logger = logger       
        self.sts = session.client('sts')
        self.ec2 = session.client('ec2', region_name=self.region)
        self.kms = session.client('kms', region_name=self.region)

    def append_item_to_list(self, items, resource_type, name, arn, region,  message=None, objs=None):
        item = None
        if not message:
            item = {
                "name": name,
                "arn": arn,
                "type": resource_type,
                "region": region
            }

        else:
            item = {
                "name" : name,
                "arn": arn,
                "type": resource_type,
                "region": region,
                "message": message
            }

        if objs:
            for obj in objs:
                item[obj['key']] = obj['value']

        items.append(item)

        return items
        
    def enabled_regions(self):
        try:
            enabled_regions = set(r['RegionName'] for r in self.ec2.describe_regions()['Regions'])

            return enabled_regions

        except ClientError as e:
            classify_error(self.logger, e, 'Failed to call ec2 describe_regions', {'region': self.region})

    def get_account_id(self):
        try:
            response = self.sts.get_caller_identity()
            
            return response['Account']

        except ClientError as e:
            classify_error(self.logger, e, 'Failed to call STS get_caller_identity', {'region': self.region})

    def find_open_ports(self, security_group, ports):

        failed = 0

        for ippermission in security_group['IpPermissions']:

            if ippermission['IpProtocol'] == '-1':
                failed = 1
            else:
                for port in ports:
                    if isinstance(port, str):
                        if port == 'icmp' and ( ippermission['IpProtocol'] == 'icmp' or ippermission['IpProtocol'] == 'icmpv6' ):
                            for iprange in ippermission['IpRanges']:
                                if iprange['CidrIp'] == "0.0.0.0/0":
                                    failed = 1

                            for iprange in ippermission['Ipv6Ranges']:
                                if iprange['CidrIpv6'] == '::/0'  :
                                    failed = 1

                    elif ippermission['FromPort'] <= port and ippermission['ToPort'] >= port :
                        for iprange in ippermission['IpRanges']:
                            if iprange['CidrIp'] == "0.0.0.0/0":
                                failed = 1

                        for iprange in ippermission['Ipv6Ranges']:
                            if iprange['CidrIpv6'] == '::/0'  :
                                failed = 1

        return failed

    def get_kms_key_details(self, keyid):
        try:
            response = self.kms.describe_key(KeyId=keyid)
            return response['KeyMetadata']

        except ClientError as e:
            classify_error(self.logger, e, 'Failed to call KMS describe_key', {'region': self.region})

    def is_integer(self, string):
        try: 
            int(string)
            return True
        except ValueError:
            return False

    def is_policy_exposed_to_everyone(self, policy):
        failed = 0
        for statement in policy['Statement']:
            if statement['Effect'] == 'Allow' :
                if isinstance(statement['Principal'], str):
                    if statement['Principal'] == '*'  and 'Condition' not in  statement:
                        failed = 1
                        break
                
                elif "AWS" in statement['Principal']:
                    if isinstance(statement['Principal']['AWS'], str):
                        statement['Principal']['AWS'] = [statement['Principal']['AWS']]

                    for principal in statement['Principal']['AWS']:
                        if principal == '*' and 'Condition' not in  statement:
                            failed = 1
                            break
            if failed:
                break
        
        return failed

    def is_policy_has_cross_account_access(self, policy):
        failed = 0
        account_id = self.get_account_id()

        for statement in policy['Statement']:
            if statement['Effect'] == 'Allow' and "AWS" in statement['Principal'] :
                if isinstance(statement['Principal']['AWS'], str):
                    statement['Principal']['AWS'] = [statement['Principal']['AWS']]

                for principal in statement['Principal']['AWS']:
                    
                    principal_split = principal.split(":")
                    
                    is_int = self.is_integer(principal)

                    if is_int and principal != account_id:
                        failed = 1
                        break

                    elif principal != '*' and account_id != principal_split[4] and 'arn:aws:iam::' in principal and ':root' in principal:
                        failed = 1
                        break

                if failed:
                    break

        return failed