from awsdeployer import gatewayres


class AmazonException(Exception):
    def __init__(self, error_code, user_message=''):
        aws_readable_msg = gatewayres.error(error_code, user_message)
        super(AmazonException, self).__init__(aws_readable_msg)
