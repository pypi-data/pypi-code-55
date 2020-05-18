import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error
from datetime import datetime, timedelta
from pytz import timezone
import pytz

class ec2handler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create EC2 client
            self.ec2_client = session.client('ec2', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create EC2 client', {'region': self.region})

        self.images = self.describe_images()
        self.instances = self.describe_instances()
        self.security_groups = self.describe_security_groups()
        self.volumes = self.describe_volumes()
        self.snapshots = self.describe_snapshots()
        self.vpcs = self.describe_vpcs()
        self.vpc_endpoints = self.describe_vpc_endpoints()
        self.key_pairs = self.describe_key_pairs()

    def describe_instances(self, filters = []):
        instances = []
        response = {}
        while True:
            try:
                if 'NextToken' in response:
                    response = self.ec2_client.describe_instances(Filters=filters, NextToken = response['NextToken'])
                else:
                    response = self.ec2_client.describe_instances(Filters=filters)

                for reservation in (response["Reservations"]):
                    for instance in reservation["Instances"]:
                        instances.append(instance)

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call EC2 describe_images', {'region': self.region})

            if 'NextToken' not in response:
                break
        
        return instances

    def describe_images(self):
        response = {}

        try:
            response = self.ec2_client.describe_images(Filters=[{'Name':'state','Values':['available']}],Owners=['self'])

            return response['Images']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call EC2 describe_images', {'region': self.region})

    def describe_snapshots(self):
        snapshots = []
        response = {}

        try:
            account_id = self.helper.get_account_id()

        except Exception as e:
            raise classify_error(self.logger, e, "Failed to get account id")

        while True:
            try:
                if 'NextToken' in response:
                    response = self.ec2_client.describe_snapshots(OwnerIds=[account_id], Filters=[{'Name': 'status', 'Values': ['completed']}], NextToken = response['NextToken'])
                else:
                    response = self.ec2_client.describe_snapshots(OwnerIds=[account_id], Filters=[{'Name': 'status', 'Values': ['completed']}])

                snapshots.extend(response['Snapshots'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call EC2 describe_snapshots', {'region': self.region})            

            if 'NextToken' not in response:
                break
        
        return snapshots

    def describe_snapshot_attribute(self, snapshotid):
        response = {}
        try:
            response = self.ec2_client.describe_snapshot_attribute(Attribute='createVolumePermission', SnapshotId=snapshotid)

            return response

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call EC2 describe_snapshot_attribute', {'region': self.region})

    def describe_security_groups(self, filters = []):
        security_groups = []
        response = {}

        while True:
            try:
                if 'NextToken' in response:
                    response = self.ec2_client.describe_security_groups(NextToken = response['NextToken'], Filters=filters)
                else:
                    response = self.ec2_client.describe_security_groups(Filters=filters)

                security_groups.extend(response['SecurityGroups'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call EC2 describe_snapshots', {'region': self.region})

            if 'NextToken' not in response:
                break
        
        return security_groups

    def describe_volumes(self):
        volumes = []
        response = {}

        while True:
            try:
                if 'NextToken' in response:
                    response = self.ec2_client.describe_volumes(NextToken = response['NextToken'])
                else:
                    response = self.ec2_client.describe_volumes()

                volumes.extend(response['Volumes'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call EC2 describe_snapshots', {'region': self.region})

            if 'NextToken' not in response:
                break
        
        return volumes

    def describe_vpcs(self):
        vpcs = []
        response = {}

        while True:
            try:
                if 'NextToken' in response:
                    response = self.ec2_client.describe_vpcs(NextToken = response['NextToken'])
                else:
                    response = self.ec2_client.describe_vpcs()

                vpcs.extend(response['Vpcs'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call EC2 describe_vpcs', {'region': self.region})

            if 'NextToken' not in response:
                break
        
        return vpcs

    def describe_flow_logs(self, filters = []):
        flow_logs = []
        response = {}

        while True:
            try:
                if 'NextToken' in response:
                    response = self.ec2_client.describe_flow_logs(Filters=filters, NextToken = response['NextToken'])
                else:
                    response = self.ec2_client.describe_flow_logs()

                flow_logs.extend(response['FlowLogs'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call EC2 describe_flow_logs', {'region': self.region})

            if 'NextToken' not in response:
                break
        
        return flow_logs

    def describe_vpc_endpoints(self):
        vpc_endpoints = []
        response = {}

        while True:
            try:
                if 'NextToken' in response:
                    response = self.ec2_client.describe_vpc_endpoints(NextToken = response['NextToken'])
                else:
                    response = self.ec2_client.describe_vpc_endpoints()

                vpc_endpoints.extend(response['VpcEndpoints'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call EC2 describe_vpc_endpoints', {'region': self.region})

            if 'NextToken' not in response:
                break
        
        return vpc_endpoints


    def describe_key_pairs(self):
        response = {}
        try:
            response = self.ec2_client.describe_key_pairs()

            return response['KeyPairs']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call EC2 describe_key_pairs', {'region': self.region})

    def ami_not_encrypted(self):
        failures = []
        failed = 0
        for image in self.images:
            for device in image['BlockDeviceMappings']:
                if 'Ebs' in device and not device['Ebs']['Encrypted']:
                    failed = 1

            if failed:
                failures = self.helper.append_item_to_list(failures, 'ec2', image['Name'], image['ImageId'] , self.region)

        return failures

    def ami_publicly_shared(self):
        failures = []
        for image in self.images:
            if image['Public']:
                failures = self.helper.append_item_to_list(failures, 'ec2', image['Name'], image['ImageId'] , self.region)

        return failures

    def default_security_group_unrestricted(self):
        failures = []

        try:
            filters=[{'Name':'group-name','Values':['default']}]
            
            security_groups = self.describe_security_groups(filters)
            
            for security_group in security_groups: 
                failed = 0
                for ippermission in security_group['IpPermissions']:

                    for iprange in ippermission['IpRanges']:
                        if iprange['CidrIp'] == "0.0.0.0/0":
                            failed = 1

                    for iprange in ippermission['Ipv6Ranges']:
                        if iprange['CidrIpv6'] == '::/0'  :
                            failed = 1
                if failed:
                    failures = self.helper.append_item_to_list(failures, 'security_groups', security_group['GroupName'], security_group['GroupId'] , self.region)


        except Exception as e:
            self.logger.error(f"Error while getting default security group details : {e}")
        return failures
    
    def default_security_group_inuse(self):
        failures = []

        try:
            filters=[{'Name':'instance.group-id','Values':['default']}]

            instances = self.describe_instances(filters)

            if len(instances) > 0 :
                msg = "Default security groups are in used. Make sure you should not use default security group."
                failures = self.helper.append_item_to_list(failures, 'security_groups', "", "" , self.region, msg)


        except Exception as e:
            self.logger.error(f"Error while getting ec2 instance details : {e}")            

        return failures

    def security_groups_rule_description_not_present(self):
        failures = []

        for security_group in self.security_groups:
            failed_for_ingress = 0
            failed_for_egress = 0
            for ippermission in security_group['IpPermissions']:
                for iprange in ippermission['IpRanges']:
                    if not iprange.get('Description'):
                        failed_for_ingress = 1
                        break

                for iprange in ippermission['Ipv6Ranges']:
                    if not iprange.get('Description'):
                        failed_for_ingress = 1
                        break

                if failed_for_ingress:
                    break

            for ippermission in security_group['IpPermissionsEgress']:
                for iprange in ippermission['IpRanges']:
                    if not iprange.get('Description'):
                        failed_for_egress = 1
                        break

                for iprange in ippermission['Ipv6Ranges']:
                    if not iprange.get('Description'):
                        failed_for_egress = 1
                        break
                    
                if failed_for_egress:
                    break

            if failed_for_ingress and failed_for_egress:
                msg = "Ingress and Egress rules do not have description defined."
                failures = self.helper.append_item_to_list(failures, 'security_groups', security_group['GroupName'], security_group['GroupId'] , self.region, msg)
            elif failed_for_ingress:
                msg = "Ingress rules do not have description defined."
                failures = self.helper.append_item_to_list(failures, 'security_groups', security_group['GroupName'], security_group['GroupId'] , self.region, msg)
            elif failed_for_egress:
                msg = "Egress rules do not have description defined."
                failures = self.helper.append_item_to_list(failures, 'security_groups', security_group['GroupName'], security_group['GroupId'] , self.region, msg)
                
        return failures

    def ami_too_old(self):
        failures = []       

        utc=pytz.UTC
        for image in self.images:
            created_on = image['CreationDate']
            created_on = datetime.strptime(created_on, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=utc)
            date_before_180_days = datetime.today() + timedelta(days=-180)
            date_before_180_days = date_before_180_days.replace(microsecond=0, tzinfo=utc)
            if created_on < date_before_180_days:
                failures = self.helper.append_item_to_list(failures, 'ec2', image['ImageId'], '-' , self.region)
        
        return failures

    def ec2_instance_not_in_vpc(self):
        failures = []
        for instance in self.instances:
            if 'VpcId' not in instance or instance['VpcId'] == '':
                failures = self.helper.append_item_to_list(failures, 'ec2', instance['InstanceId'], instance['InstanceId'] , self.region)

        return failures

    def ec2_instances_not_using_iam_role(self):
        failures = []

        for instance in self.instances:
            if 'IamInstanceProfile' not in instance:
                failures = self.helper.append_item_to_list(failures, 'ec2', instance['InstanceId'], instance['InstanceId'] , self.region)
        
        return failures

    def security_group_prefixed_with_launch_wizard(self):
        failures = []

        try:
            filters= [{'Name':'group-name','Values':['launch-wizard-*']}]
            
            security_groups = self.describe_security_groups(filters)
            
            for security_group in security_groups:                 
                failures = self.helper.append_item_to_list(failures, 'security_groups', security_group['GroupName'], security_group['GroupId'] , self.region)

        except Exception as e:
            self.logger.error(f"Error while getting default security group details : {e}")

        return failures

    def security_group_open_port_range(self):
        failures = []

        for security_group in self.security_groups:
            for ippermission in security_group['IpPermissions']:
                if ippermission['IpProtocol'] != '-1' and ippermission['FromPort'] != ippermission['ToPort']:
                    failures = self.helper.append_item_to_list(failures, 'security_groups', security_group['GroupName'], security_group['GroupId'] , self.region)
                elif ippermission['IpProtocol'] == '-1' :
                    failures = self.helper.append_item_to_list(failures, 'security_groups', security_group['GroupName'], security_group['GroupId'] , self.region)
        
        return failures

    def find_unrestricted_open_ports(self, parameters):
        failures = []
        for security_group in self.security_groups:
            result = self.helper.find_open_ports(security_group, parameters['ports'])
            if result:
                failures = self.helper.append_item_to_list(failures, 'security_groups', security_group['GroupName'], security_group['GroupId'] , self.region)
                 
        return failures

    def unrestricted_outbound_access_for_all_ports(self):
        failures = []
        for security_group in self.security_groups:            
            failed = 0
            for ippermission in security_group['IpPermissionsEgress']:

                for iprange in ippermission['IpRanges']:
                    if iprange['CidrIp'] == "0.0.0.0/0":
                        failed = 1

                for iprange in ippermission['Ipv6Ranges']:
                    if iprange['CidrIpv6'] == '::/0'  :
                        failed = 1

            if failed:
                failures = self.helper.append_item_to_list(failures, 'security_groups', security_group['GroupName'], security_group['GroupId'] , self.region)

        return failures

    def unused_key_pairs(self):
        failures = []

        for key_pair in self.key_pairs:

            try:
                filter = [{'Name': 'key-name', 'Values': [ key_pair['KeyName'] ]}]
                instances = self.describe_instances(filter)

                if len(instances) == 0:
                    failures = self.helper.append_item_to_list(failures, 'key_pairs', key_pair['KeyName'], key_pair['KeyPairId'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting instance details : {e}")
            
        return failures
    
    def ebs_public_snapshot(self):
        failures = []

        for snapshot in self.snapshots:
            try:
                response = self.describe_snapshot_attribute(snapshot['SnapshotId'])
                for permission in response['CreateVolumePermissions']:
                    if 'Group' in permission and permission['Group'] == 'all':
                        failures = self.helper.append_item_to_list(failures, 'snapshots', snapshot['SnapshotId'], snapshot['SnapshotId'] , self.region)
            except Exception as e:
                self.logger.error(f"Error while getting snapshot attribute details for snapshot - {snapshot['SnapshotId']}: {e}")
                
        return failures
    
    def ebs_volume_not_encrypted(self):
        failures = []

        for volume in self.volumes:
            if not volume['Encrypted']:
                failures = self.helper.append_item_to_list(failures, 'volumes', volume['VolumeId'], volume['VolumeId'] , self.region)
        return failures
    
    def ebs_volume_not_encrypted_with_kms_cmk(self):
        failures = []

        for volume in self.volumes:
            try:
                if volume.get('KmsKeyId'):
                    response = self.helper.get_kms_key_details(volume['KmsKeyId'])
                    if response['KeyManager'] != 'CUSTOMER' : 
                        failures = self.helper.append_item_to_list(failures, 'volumes', volume['VolumeId'], volume['VolumeId'] , self.region)
                elif not volume['Encrypted']:
                    failures = self.helper.append_item_to_list(failures, 'volumes', volume['VolumeId'], volume['VolumeId'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting kms key details for volume - { volume['VolumeId'] }: {e}")
            
        return failures

    def ebs_snapshot_not_encrypted(self):
        failures = []

        for snapshot in self.snapshots:
            if not snapshot['Encrypted']:
                failures = self.helper.append_item_to_list(failures, 'snapshots', snapshot['SnapshotId'], snapshot['SnapshotId'] , self.region)

        return failures

    def vpc_endpoint_cross_account_access_enabled(self):
        failures = []

        for vpc_endpoint in self.vpc_endpoints:
            policy_document = json.loads(vpc_endpoint['PolicyDocument'])            
            if policy_document != "":
                have_caa_enabled = self.helper.is_policy_has_cross_account_access(policy_document)
                if have_caa_enabled:
                    failures = self.helper.append_item_to_list(failures, 'vpc', vpc_endpoint['VpcEndpointId'], vpc_endpoint['VpcEndpointId'] , self.region)
        return failures

    def vpc_endpoint_exposed(self):
        failures = []

        for vpc_endpoint in self.vpc_endpoints:
            policy_document = json.loads(vpc_endpoint['PolicyDocument'])
            if policy_document != "":
                is_exposed = self.helper.is_policy_exposed_to_everyone(policy_document)
                if is_exposed:
                    failures = self.helper.append_item_to_list(failures, 'vpc', vpc_endpoint['VpcEndpointId'], vpc_endpoint['VpcEndpointId'] , self.region)
        return failures

    def vpc_flowlog_not_enabled(self):
        failures = []

        for vpc in self.vpcs:

            try:
                filter = [{'Name':'resource-id','Values':[vpc['VpcId']]}]
                response = self.describe_flow_logs(filter)

                if len(response) == 0 :
                    failures = self.helper.append_item_to_list(failures, 'vpc', vpc['VpcId'], vpc['VpcId'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting flow logs details for VPC - { vpc['VpcId'] }: {e}")

        return failures

    def default_vpc_exists(self):
        failures = []

        for vpc in self.vpcs:
            if vpc['IsDefault']:
                failures = self.helper.append_item_to_list(failures, 'vpc', vpc['VpcId'], vpc['VpcId'], self.region)

        return failures

    # def default_vpc_in_use(self):
    #     failures = []
    #     return failures