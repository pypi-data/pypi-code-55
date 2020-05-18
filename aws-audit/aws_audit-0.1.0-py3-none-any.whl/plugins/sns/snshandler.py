import json, os
# from botocore.exceptions import ClientError
# import boto3
from aws_audit.helper.common import CommonHelper
from aws_audit.utils.errors import classify_error

class snshandler : 

    def __init__(self, session, region, logger):
        
        self.logger = logger
        self.region = region
        self.helper = CommonHelper(session, region, logger)
        
        try:
            # Create SNS client
            self.sns_client = session.client('sns', region_name=region)
            
        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to create SNS client', {'region': self.region})
        
        self.topics = self.list_topics()

    # Get list of all topics
    def list_topics(self):
        topics = []
        response = {}

        while True:

            try:
                if 'NextToken' in response:
                    response = self.sns_client.list_topics(NextToken=response['NextToken'])
                else:
                    response = self.sns_client.list_topics()

                topics.extend(response['Topics'])

            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call SNS list_topics', {'region': self.region})

            if 'NextToken' not in response:
                break

        return topics

    # Get  attribute details for topic
    def get_topic_attribute_details(self, topic_arn, attribute):
        try:
            response = self.sns_client.get_topic_attributes(TopicArn=topic_arn)

            if attribute in response['Attributes']:
                return response['Attributes'][attribute]
            else:
                return ''

        except Exception as e:
            raise classify_error(self.logger, e, 'Failed to call SNS get_topic_attributes', {'region': self.region})
    
    # Get all subscriptions for topic
    def list_subscriptions_by_topic(self, topic_arn):
        
        subscriptions = []
        response = {}

        while True:

            try:
                if 'NextToken' in response:
                    response = self.sns_client.list_subscriptions_by_topic(TopicArn=topic_arn,NextToken=response['NextToken'])
                else:
                    response = self.sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)

                subscriptions.extend(response['Subscriptions'])
               
            except Exception as e:
                raise classify_error(self.logger, e, 'Failed to call SNS list_subscriptions_by_topic', {'region': self.region})

            if 'NextToken' not in response:
                break
                
        return subscriptions

    def sns_topics_not_encrypted(self):
        failures = []
        for topic in self.topics:
            try:
                kms_key_id = self.get_topic_attribute_details(topic['TopicArn'],'KmsMasterKeyId')
                if kms_key_id == '':
                    failures = self.helper.append_item_to_list(failures, 'sns', topic['TopicArn'], topic['TopicArn'] , self.region)

            except Exception as e:                
                self.logger.error(f"Error while getting attribute for topic {topic['TopicArn']}: {e}")

        return failures

    def sns_topics_not_encrypted_with_kms_cmk(self):
        failures = []
        for topic in self.topics:
            try:

                kms_key_id = self.get_topic_attribute_details(topic['TopicArn'],'KmsMasterKeyId')
                if kms_key_id != '' and kms_key_id == 'alias/aws/sns':
                    failures = self.helper.append_item_to_list(failures, 'sns', topic['TopicArn'], topic['TopicArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting attribute for topic {topic['TopicArn']}: {e}")
            
        return failures

    def sns_topic_is_exposed(self):
        failures = []
        for topic in self.topics:
            try:
                policy = self.get_topic_attribute_details(topic['TopicArn'],'Policy')
                policy_document = json.loads(policy)
                is_exposed = self.helper.is_policy_exposed_to_everyone(policy_document)
                if is_exposed:
                    failures = self.helper.append_item_to_list(failures, 'sns', topic['TopicArn'], topic['TopicArn'] , self.region)

            except Exception as e:
                self.logger.error(f"Error while getting attribute for topic {topic['TopicArn']}: {e}")
                continue
                
        return failures

    def sns_topic_have_cross_account_access(self):
        failures = []

        for topic in self.topics:
            try:
                policy = self.get_topic_attribute_details(topic['TopicArn'],'Policy')
                policy_document = json.loads(policy)
                is_caa_enabled = self.helper.is_policy_has_cross_account_access(policy_document)
                if is_caa_enabled:
                    failures = self.helper.append_item_to_list(failures, 'sns', topic['TopicArn'], topic['TopicArn'] , self.region)  

            except Exception as e:
                self.logger.error(f"Error while getting attribute for topic {topic['TopicArn']}: {e}")
                continue
                
        return failures

    def sns_topic_using_insecure_subscription(self):
        failures = []
        for topic in self.topics:
            try:
                subscriptions = self.list_subscriptions_by_topic(topic['TopicArn'])
                insecure_subscription = 0
                for subscription in subscriptions:
                    if subscription['Protocol'] == 'http' :
                        insecure_subscription = 1
                
                if insecure_subscription:
                    failures = self.helper.append_item_to_list(failures, 'sns', topic['TopicArn'], topic['TopicArn'] , self.region)  

            except Exception as e:
                self.logger.error(f"Error while checking subscription for topic {topic['TopicArn']}: {e}")
                
        return failures

    def sns_topic_allows_eveyone_to_publish(self):
        failures = []
        for topic in self.topics:
            try:
                policy = self.get_topic_attribute_details(topic['TopicArn'],'Policy')
                policy_document = json.loads(policy)
                for statement in policy_document['Statement']:
                    if 'AWS' in statement['Principal']:
                        if statement['Effect'] == 'Allow' and statement['Principal']['AWS'] == '*' and statement['Action'] == 'SNS:Publish' and statement['Resource'] == topic['TopicArn'] and 'Condition' not in statement:
                            failures = self.helper.append_item_to_list(failures, 'sns', topic['TopicArn'], topic['TopicArn'] , self.region)  
            except Exception as e:
                self.logger.error(f"Error while checking attribute for topic {topic['TopicArn']}: {e}")

        return failures

    def sns_topic_allows_eveyone_to_subscribe(self):
        failures = []
        for topic in self.topics:
            try:

                policy = self.get_topic_attribute_details(topic['TopicArn'],'Policy')
                policy_document = json.loads(policy)
                action_rule  = ["SNS:Receive","SNS:Subscribe"] 
                for statement in policy_document['Statement']:
                    
                    statement_action = []
                    if isinstance(statement['Action'], list):
                        statement_action = statement['Action']
                        statement_action.sort()
                    else :
                        statement_action.append(statement['Action'])
                    
                    if 'AWS' in statement['Principal']:
                        if statement['Effect'] == 'Allow' and statement['Principal']['AWS'] == '*' and action_rule == statement_action  and statement['Resource'] == topic['TopicArn'] and 'Condition' not in statement:
                            failures = self.helper.append_item_to_list(failures, 'sns', topic['TopicArn'], topic['TopicArn'] , self.region)  

            except Exception as e:
                self.logger.error(f"Error while checking attribute for topic {topic['TopicArn']}: {e}")

        return failures
