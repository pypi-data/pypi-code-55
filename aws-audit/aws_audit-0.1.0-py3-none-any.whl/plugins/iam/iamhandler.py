import json, os
from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error
from time import sleep
from collections import namedtuple

class iamhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create IAM client
            self.iam_client = session.client('iam', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create IAM client', {'region': self.region})

        self.users = self.list_users()
        self.groups = self.list_groups()
        self.policies = self.list_policies()

        self.credential_report = {}

    def list_users(self):
        users = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.iam_client.list_users(Marker=response['Marker'])
                else:
                    response = self.iam_client.list_users()

                users.extend(response['Users'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call IAM list_users', {'region': self.region})

            if 'Marker' not in response:
                break

        return users

    def list_groups(self):
        groups = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.iam_client.list_groups(Marker=response['Marker'])
                else:
                    response = self.iam_client.list_groups()

                groups.extend(response['Groups'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call IAM list_groups', {'region': self.region})

            if 'Marker' not in response:
                break

        return groups

    def list_policies(self):
        policies = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.iam_client.list_policies(Scope='Local', Marker=response['Marker'])
                else:
                    response = self.iam_client.list_policies(Scope='Local')

                policies.extend(response['Policies'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call IAM list_policies', {'region': self.region})

            if 'Marker' not in response:
                break

        return policies

    def get_account_password_policy(self):
        try:
            response = self.iam_client.get_account_password_policy()

            return response['PasswordPolicy']

        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                return {}
            else:
                raise classify_error(self.logger, e, 'Failed to get account password policy.', {'region': self.region})

    def get_login_profile(self, username):
        try:
            response = self.iam_client.get_login_profile(UserName=username)

            return response['LoginProfile']

        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                return {}
            else:
                raise classify_error(self.logger, e, 'Failed to get login profile.', {'region': self.region})

    def list_attached_user_policies(self, username):
        user_policies = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.iam_client.list_attached_user_policies(UserName=username, Marker=response['Marker'])
                else:
                    response = self.iam_client.list_attached_user_policies(UserName=username)

                user_policies.extend(response['AttachedPolicies'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call IAM list_attached_user_policies', {'region': self.region})

            if 'Marker' not in response:
                break

        return user_policies

    def list_group_policies(self, groupname):
        group_policies = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.iam_client.list_group_policies(GroupName=groupname, Marker=response['Marker'])
                else:
                    response = self.iam_client.list_group_policies(GroupName=groupname)

                group_policies.extend(response['PolicyNames'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call IAM list_group_policies', {'region': self.region})

            if 'Marker' not in response:
                break

        return group_policies

    def get_policy_version(self, policy, version):
        try:
            response = self.iam_client.get_policy_version(PolicyArn=policy, VersionId=version)

            return response['PolicyVersion']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call IAM get_policy_version', {'region': self.region})
    
    def list_mfa_devices(self, username):
        
        mfa_devices = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.iam_client.list_mfa_devices(UserName=username, Marker=response['Marker'])
                else:
                    response = self.iam_client.list_mfa_devices(UserName=username)

                mfa_devices.extend(response['MFADevices'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call IAM list_mfa_devices', {'region': self.region})

            if 'Marker' not in response:
                break

        return mfa_devices

    def list_access_keys(self, username):
        access_keys = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.iam_client.list_access_keys(UserName=username, Marker=response['Marker'])
                else:
                    response = self.iam_client.list_access_keys(UserName=username)

                access_keys.extend(response['AccessKeyMetadata'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call IAM list_access_keys', {'region': self.region})

            if 'Marker' not in response:
                break

        return access_keys

    def list_ssh_public_keys(self, username):
        ssh_keys = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.iam_client.list_ssh_public_keys(UserName=username, Marker=response['Marker'])
                else:
                    response = self.iam_client.list_ssh_public_keys(UserName=username)

                ssh_keys.extend(response['SSHPublicKeys'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call IAM list_ssh_public_keys', {'region': self.region})
            if 'Marker' not in response:
                break

        return ssh_keys

    def get_group(self, groupname):
        group_users = []
        response = {}

        while True:

            try:
                if 'Marker' in response:
                    response = self.iam_client.get_group(GroupName=groupname, Marker=response['Marker'])
                else:
                    response = self.iam_client.get_group(GroupName=groupname)

                group_users.extend(response['Users'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call IAM get_group', {'region': self.region})

            if 'Marker' not in response:
                break

        return group_users

    def generate_credential_report(self):
        
        response = {}

        while True:
            try:

                response = self.iam_client.generate_credential_report()

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call IAM generate_credential_report', {'region': self.region})
            
            if response['State'] != 'COMPLETE' :
                sleep(30)
            else:
                break
        
        return response
        

    def get_credential_report(self):
        

        try:
            report = self.generate_credential_report()        
        except Exception as e:
            return {}

        try:
            if report['State'] == 'COMPLETE':
                response = self.iam_client.get_credential_report()

                return response

            else:
                return {}

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call IAM get_credential_report', {'region': self.region})

    def parse_credential_report(self, content):
        User = namedtuple('User', 'user arn user_creation_time password_enabled password_last_used password_last_changed password_next_rotation mfa_active access_key_1_active access_key_1_last_rotated access_key_1_last_used_date access_key_1_last_used_region access_key_1_last_used_service access_key_2_active access_key_2_last_rotated access_key_2_last_used_date access_key_2_last_used_region access_key_2_last_used_service cert_1_active cert_1_last_rotated cert_2_active cert_2_last_rotated')

        body = content.decode('utf-8')
        lines = body.split('\n')
        users = [User(*line.split(',')) for line in lines[1:]]
        return users
    
    def iam_password_policy_not_defined(self):

        failures = []

        try:
            reponse = self.get_account_password_policy()

            if len(reponse) == 0:
                msg = 'Password policy for account is not defined. Please make sure you have strong password policy defined.'
                failures = self.helper.append_item_to_list(failures, 'iam', '', '' , self.region, msg)


        except Exception as e:
            self.logger.error(f"Error while getting account password policy : {e}")

        return failures

    def iam_users_with_full_administrator_permission(self):
        failures = []
        for user in self.users:
            try:
                policies = self.list_attached_user_policies(user['UserName'])

                for policy in policies:
                    if policy['PolicyName'] == 'AdministratorAccess':
                        failures = self.helper.append_item_to_list(failures, 'iam', user['UserName'], user['Arn'], self.region)
            except Exception as e:
                self.logger.error(f"Error while getting user policies : {e}")

        return failures

    def iam_policy_with_full_administrator_access(self):

        failures = []

        for policy in self.policies:

            try:
                response = self.get_policy_version(policy['Arn'], policy['DefaultVersionId'])

                policy_document = json.dumps(response['Document'])
                policy_document = json.loads(policy_document)

                for statement in policy_document['Statement']:
                    if ( isinstance(statement['Action'], str) and statement['Action'] == '*' )  and statement['Effect'] == 'Allow' and ( isinstance(statement['Resource'], str) and statement['Resource'] == '*'):
                        failures = self.helper.append_item_to_list(failures, 'iam', policy['PolicyName'], policy['Arn'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting policy document : {e}")
        
        return failures     

    def iam_group_with_inline_policy(self):
        failures = []

        for group in self.groups:
            try:
                response = self.list_group_policies(group['GroupName'])
                if len(response) > 0:
                    failures = self.helper.append_item_to_list(failures, 'iam', group['GroupName'], group['Arn'], self.region)
            except Exception as e:
                self.logger.error(f"Error while getting inline policies for group : {e}")

        return failures

    def iam_users_not_present(self):
        failures = []
        if len(self.users) == 0 :
            msg = "Their is no IAM users present in your account. Make sure that at least one IAM user in your account."
            failures = self.helper.append_item_to_list(failures, 'iam', "", "", self.region, msg)

        return failures

    def iam_mfa_not_enabled_for_users(self):
        failures = []

        for user in self.users:
            try:
                user_able_to_login = self.get_login_profile(user['UserName'])
                if user_able_to_login :
                    response = self.list_mfa_devices(user['UserName'])
                    if not response:
                        failures = self.helper.append_item_to_list(failures, 'iam', user['UserName'], user['Arn'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting MFA devices for user : {e}")

        return failures

    def iam_root_account_access_key_present(self):
        failures = []

        try:
            response = self.get_credential_report()
        except Exception as e:
            self.logger.error(f"Error while getting credential report : {e}")

        if response:
            users = self.parse_credential_report(response['Content'])

            for user in users:
                if user.user == '<root_account>' and ( user.access_key_1_active == 'true' or user.access_key_2_active == 'true' ):
                    msg = "Root account access key is present."
                    failures = self.helper.append_item_to_list(failures, 'iam', user.user, user.arn, self.region, msg)
                    break
        
        return failures

    def iam_root_account_mfa_not_enabled(self):
        failures = []

        try:
            response = self.get_credential_report()
        except Exception as e:
            self.logger.error(f"Error while getting credential report : {e}")

        if response:
            users = self.parse_credential_report(response['Content'])

            for user in users:
                if user.user == '<root_account>' and user.mfa_active == 'false':
                    msg = "Root account MFA is not enabled. Make sure root account has MFA enabled."
                    failures = self.helper.append_item_to_list(failures, 'iam', user.user, user.arn, self.region, msg)
                    break
        
        return failures

    def iam_user_has_more_than_one_active_access_keys(self):
        failures = []
        for user in self.users:
            try:
                access_keys = self.list_access_keys(user['UserName'])
                count = 0
                for access_key in access_keys:
                    if access_key['Status'] == 'Active':
                        count = count + 1
                if count > 1:
                    failures = self.helper.append_item_to_list(failures, 'iam', user['UserName'], user['Arn'], self.region)
            except Exception as e:
                self.logger.error(f"Error while getting access keys for user : {e}")

        return failures

    def iam_user_has_more_than_one_active_ssh_keys(self):
        failures = []
        for user in self.users:
            try:
                ssh_keys = self.list_ssh_public_keys(user['UserName'])
                count = 0
                for ssh_key in ssh_keys:
                    if ssh_key['Status'] == 'Active':
                        count = count + 1
                if count > 1:
                    failures = self.helper.append_item_to_list(failures, 'iam', user['UserName'], user['Arn'], self.region)
            except Exception as e:
                self.logger.error(f"Error while getting ssh keys for user : {e}")

        return failures

    def iam_unused_groups(self):
        failures = []
        
        for group in self.groups:
            try:
                users = self.get_group(group['GroupName'])
                if not users:
                    failures = self.helper.append_item_to_list(failures, 'iam', group['GroupName'], group['Arn'], self.region)

            except Exception as e:
                self.logger.error(f"Error while getting group details : {e}")
        
        return failures

    def iam_unused_users(self):
        failures = []

        try:
            response = self.get_credential_report()
        except Exception as e:
            self.logger.error(f"Error while getting credential report : {e}")

        if response:
            users = self.parse_credential_report(response['Content'])

            for user in users:
                if user.user == '<root_account>':
                    continue
                if user.password_enabled == 'false':
                    continue
                
                not_logged_in = 0
                no_access_key = 0
                if user.password_last_used == 'no_information':
                    not_logged_in = 1
                
                try:
                    access_keys = self.list_access_keys(user.user)
                    if not access_keys:
                        no_access_key = 1
                    
                except Exception as e:
                    self.logger.error(f"Error while getting access keys for user : {e}")

                if not_logged_in and no_access_key:
                    failures = self.helper.append_item_to_list(failures, 'iam', user.user , user.arn, self.region)
                
        return failures