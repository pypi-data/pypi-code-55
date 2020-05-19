import boto3


class SSMClient:
    def __init__(self, config, **client_kwargs):
        self.session = boto3.Session(**client_kwargs)

        self.ssm_config = config
        self.profile_name = 'default'

    def client(self):
        return self.session.client('ssm')

    def get(self, name):
        return self.client().get_parameter(
            Name=name,
            WithDecryption=self.ssm_config.should_auto_decrypt_secret_value()
        )['Parameter']['Value']

    def describe(self, parameters_path=''):
        if parameters_path:
            params = self.client().describe_parameters(ParameterFilters=[
                {
                    'Key': 'Path',
                    'Values': [
                        parameters_path,
                    ]
                },
            ])['Parameters']
        else:
            params = self.client().describe_parameters()['Parameters']

        return [key['Name'] for key in params]

    def put(self, key, value, description):
        self.client().put_parameter(
            Name=key,
            Description=description,
            Value=value,
            Type='SecureString' if self.ssm_config.should_auto_encrypt_secret_value() else 'String'
        )
