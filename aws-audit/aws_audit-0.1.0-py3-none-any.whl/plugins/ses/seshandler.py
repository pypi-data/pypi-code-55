import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error


class seshandler : 
    
    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create SES client
            self.ses_client = session.client('ses', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create SES client', {'region': self.region})
        
        
        self.identities = self.list_identities()

    def list_identities(self):
        identities = []
        response = {}
        while True:
            try:
                if 'NextToken' in response:
                    response = self.ses_client.list_identities(NextToken = response['NextToken'])
                else:
                    response = self.ses_client.list_identities()

                identities.extend(response['Identities'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call SES list_secrets', {'region': self.region})

            if 'NextToken' not in response:
                break
        
        return identities
        
    # get identity dkim attributes
    def get_identity_dkim_attributes(self):
        try:
            response = self.ses_client.get_identity_dkim_attributes(Identities=self.identities)

            return response['DkimAttributes']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call SES get_identity_dkim_attributes', {'region': self.region})

     # get list of identity policies
    def list_identity_policies(self, identity) : 
        try:
            response = self.ses_client.list_identity_policies(Identity=identity)

            return response['PolicyNames']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call SES list_identity_policies', {'region': self.region})
    
    # get json policy for indentiy 
    def get_identity_policies(self, identity, policies):
        try:
            response = self.ses_client.get_identity_policies(Identity=identity,PolicyNames=policies)

            return response['Policies']

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call SES get_identity_policies', {'region': self.region})

    # check if dkim is enabled
    def ses_dkim_not_enabled(self):
        failures = []
        try:
            dkim_attributes = self.get_identity_dkim_attributes()
            for identity in dkim_attributes:
                if not dkim_attributes[identity]['DkimEnabled']:
                    failures = self.helper.append_item_to_list(failures, 'ses', identity, identity, self.region)
        except Exception as e:
            self.logger.error(f"Error while checking DKIM is enabled : {e}")

        return failures

    def ses_identities_exposed(self):
        failures = []
        for identity in self.identities:
            try:
                policies = self.list_identity_policies(identity)
                if policies:
                    policy_document = self.get_identity_policies(identity,policies)
                    is_exposed = 0
                    for policy in policy_document:
                        policy_statements = json.loads(policy_document[policy])
                        is_exposed = self.helper.is_policy_exposed_to_everyone(policy_statements)
                        if is_exposed:
                            break
                    if is_exposed:
                        failures = self.helper.append_item_to_list(failures, 'ses', identity, identity, self.region)
                                
            except Exception as e:
                self.logger.error(f"Error while getting identity policies - {identity}: {e}")
                continue
                
        return failures

    def ses_identities_allow_cross_account_access(self):
        failures = []

        for identity in self.identities:
            try:
                policies = self.list_identity_policies(identity)
                is_caa_enabled = 0 
                if policies:
                    policy_documents = self.get_identity_policies(identity,policies)
                    for policy in policy_documents:
                        policy_statements = json.loads(policy_documents[policy])
                        is_caa_enabled = self.helper.is_policy_has_cross_account_access(policy_statements)
                        if is_caa_enabled:
                            break
                if is_caa_enabled:
                    failures = self.helper.append_item_to_list(failures, 'ses', identity, identity, self.region)
            
            except Exception as e:
                self.logger.error(f"Error while getting identity policies - {identity}: {e}")
                continue
        
        return failures
        