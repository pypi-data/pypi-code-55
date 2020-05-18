import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class shieldhandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create Shield client
            self.shield_client = session.client('shield', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create Shield client', {'region': self.region})

    def shield_advance_not_enabled(self):
        failures = []
        try:
            state = self.shield_client.get_subscription_state()
            if state['SubscriptionState'] == 'INACTIVE':
                msg = 'AWS Advance Shield is not enabled.'
                failures = self.helper.append_item_to_list(failures, 'shield', "", "", self.region, msg)
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call Shield get_subscription_state', {'region': self.region})

        return failures
