import json, os
from botocore.exceptions import ClientError
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class backuphandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Backup client
            self.backup_client = session.client('backup', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Backup client', {'region': self.region})

        self.backup_vaults = self.list_backup_vaults()
        self.backup_plans = self.list_backup_plans()
        
    def list_backup_vaults(self):
        backup_vaults = []
        response = {}

        while True:

            try:
                if 'NextToken' in response:
                    response = self.backup_client.list_backup_vaults(NextToken = response['NextToken'])
                else:
                    response = self.backup_client.list_backup_vaults()

                backup_vaults.extend(response['BackupVaultList'])                

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Backup list_backup_vaults', {'region': self.region})            

            if 'NextToken' not in response:
                break

        return backup_vaults

    def get_backup_vault_access_policy(self, backup_vault_name):
        try:
            response = self.backup_client.get_backup_vault_access_policy(BackupVaultName=backup_vault_name)

            return response
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                return {}
            else:
                raise classify_error(self.logger, e, 'Failed to call Backup get_backup_vault_access_policy', {'region': self.region})

    def list_backup_plans(self):
        backup_plans = []
        response = {}

        while True:

            try:
                if 'NextToken' in response:
                    response = self.backup_client.list_backup_plans(NextToken = response['NextToken'])
                else:
                    response = self.backup_client.list_backup_plans()

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call Backup list_backup_plans', {'region': self.region})
            
            backup_plans.extend(response['BackupPlansList'])

            if 'NextToken' not in response:
                break

        return backup_plans

    def get_backup_plan(self, backup_plan_id, version_id):
        try:
            response = self.backup_client.get_backup_plan(BackupPlanId=backup_plan_id, VersionId=version_id)

            return response['BackupPlan']['Rules']

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                return {}
            else:
                raise classify_error(self.logger, e, 'Failed to call Backup get_backup_plan', {'region': self.region})

    def backup_vault_access_policy_not_defined_to_prevent_deletion(self):
        failures = []

        for vault in self.backup_vaults:
            try:
                policy = self.get_backup_vault_access_policy(vault['BackupVaultName'])
                if not policy:
                    msg = "Access policy not defined for back vault."
                    failures = self.helper.append_item_to_list(failures, 'backup', vault['BackupVaultName'], vault['BackupVaultArn'] , self.region, msg)
                else:
                    failed = 1
                    for statement in policy['Statement']:
                        if isinstance(statement['Action'], str):
                            statement['Action'] = [statement['Action']]

                        if isinstance(statement['Resource'], str):
                            statement['Resource'] = [statement['Resource']]
                        
                        if 'backup:DeleteRecoveryPoint' in statement['Action']  and vault['BackupVaultArn'] in statement['Resource']:
                            failed = 0
                            break
                    
                    if failed:
                        failures = self.helper.append_item_to_list(failures, 'backup', vault['BackupVaultName'], vault['BackupVaultArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting Backup access policy: {e}")

        return failures

    def backup_vault_not_encrypted_with_kms_cmk(self):
        failures = []

        for vault in self.backup_vaults:
            key = vault['EncryptionKeyArn'].split('/')
            key_details = self.helper.get_kms_key_details(key[1])
            if key_details['KeyManager'] != 'CUSTOMER':
                failures = self.helper.append_item_to_list(failures, 'backup', vault['BackupVaultName'], vault['BackupVaultArn'] , self.region)

        return failures

    def backup_plan_lifecycle_configuration_not_enabled(self):
        failures = []

        for plan in self.backup_plans:
            try:
                plan_details = self.get_backup_plan(plan['BackupPlanId'], plan['VersionId'])
                if plan_details:
                    for rule in plan_details:
                        if 'Lifecycle' not in rule:
                            failures = self.helper.append_item_to_list(failures, 'backup', plan['BackupPlanId'], plan['BackupPlanArn'] , self.region)
            
            except Exception as e:
                self.logger.error(f"Error while getting Backup plan details: {e}")

        return failures