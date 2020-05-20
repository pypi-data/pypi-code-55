import logging
from time import sleep

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class Manager:
    _client = None
    _username = None
    aws_access_key_id = None
    aws_secret_access_key = None
    aws_session_token = None

    def __init__(
        self,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_session_token=None,
        username=None,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        self._username = username

        if self.aws_access_key_id is None:
            # Discover the key being used in a shared credentials file
            self._use_first_active_key()

    @property
    def client(self):
        if self._client is None:
            self._client = boto3.client(
                'iam',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
            )
        return self._client

    @property
    def username(self):
        if self._username is None:
            self._username = self.keys()[0]['UserName']
        return self._username

    def _use_first_active_key(self):
        for key in self.keys():
            if key['Status'] == 'Active':
                self.aws_access_key_id = key['AccessKeyId']
                self.aws_secret_access_key = None
                self.aws_session_token = None
                self._username = key['UserName']
                break

    def keys(self):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_access_keys
        logger.debug("Fetching keys using {}".format(self.aws_access_key_id))
        keys = self.client.list_access_keys()
        return keys['AccessKeyMetadata']

    def create(self):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_access_key
        logger.debug("Creating key using {}".format(self.aws_access_key_id))
        response = self.client.create_access_key(UserName=self.username)
        return response

    def activate(self, access_key):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_access_key
        logger.debug("Activating key {} using {}".format(
            access_key,
            self.aws_access_key_id
        ))
        response = self.client.update_access_key(
            UserName=self.username,
            AccessKeyId=access_key,
            Status='Active',
        )
        response.setdefault('AccessKey', {}).setdefault('AccessKeyId', access_key)
        return response

    def deactivate(self, access_key):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_access_key
        logger.debug("Deactivating key {} using {}".format(
            access_key,
            self.aws_access_key_id
        ))
        response = self.client.update_access_key(
            UserName=self.username,
            AccessKeyId=access_key,
            Status='Inactive',
        )
        response.setdefault('AccessKey', {}).setdefault('AccessKeyId', access_key)
        return response

    def delete(self, access_key):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_access_key
        logger.debug("Deleting key {} using {}".format(
            access_key,
            self.aws_access_key_id
        ))
        response = self.client.delete_access_key(
            UserName=self.username,
            AccessKeyId=access_key,
        )
        response.setdefault('AccessKey', {}).setdefault('AccessKeyId', access_key)
        return response

    def rotate(self):
        # AWS has a limit of 2 keys
        new_key = deleted_key = deactivated_key = None
        try:
            new_key = self.create()
        except ClientError as e:
            if e.response.get('Error', {}).get('Code') != 'LimitExceeded':
                raise
            deleted_key = self.delete_inactive()
            new_key = self.create()

        access_key = new_key['AccessKey']['AccessKeyId']
        secret_key = new_key['AccessKey']['SecretAccessKey']
        username = new_key['AccessKey']['UserName']

        # Always fails right away, so have an initial sleep
        logger.debug('Pausing to allow keys to propagate')
        sleep(8)

        new_mgr = Manager(aws_access_key_id=access_key, aws_secret_access_key=secret_key, username=username)
        for attempt in range(3):
            try:
                deactivated_key = new_mgr.deactivate(self.aws_access_key_id)
                break
            except ClientError as e:
                if e.response.get('Error', {}).get('Code') != 'InvalidClientTokenId':
                    raise
                length = 2 ** (attempt + 1)
                logger.debug("Pausing for additional {}s to allow keys to propagate".format(
                    length
                ))
                sleep(length)
        else:
            logger.warn("Timed out attempting to deactivate {}".format(self.aws_access_key_id))

        # make sure this manager has the new keys
        self.aws_access_key_id = access_key
        self.aws_secret_access_key = secret_key
        self._client = None

        return {
            'new_key': new_key,
            'deleted_key': deleted_key,
            'deactivated_key': deactivated_key,
        }

    def delete_inactive(self):
        # AWS has a limit of 2 keys
        for key in self.keys():
            if key['Status'] != 'Inactive':
                continue
            logger.debug("Deleting inactive key: {}".format(key['AccessKeyId']))
            return self.delete(key['AccessKeyId'])
        raise RuntimeError('No inactive keys')
