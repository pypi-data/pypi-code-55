import os, json
from dotenv import load_dotenv

class Configure:

    def __init__(self, logger):
        self.logger = logger
        self.configuration_file = self.get_configuration_file_path()

    def set_configuartion(self):
        self.logger.info(f"Setting configuration for aws-audit...")
        if self.verify_configuration_file():
            AWS_ACCESS_KEY_ID = input("Provide AWS Access Key ID: ")
            AWS_SECRET_ACCESS_KEY = input("Provide AWS Secret Access Key: ")
            params = {
                'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
                'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY
            }
            self.write_configuration(params)        

    def get_configuration_file_path(self):
        self.logger.info(f"Getting configuration file path.")
        home = os.path.expanduser('~')
        location = os.path.join(home, '.audit')
        credential_file = os.path.join(location, 'configure')
        return credential_file

    def verify_configuration_file(self):
        self.logger.info(f"veify configuration file path.")
        if not os.path.exists(self.configuration_file):
            os.makedirs(os.path.dirname(self.configuration_file), exist_ok=True)
            return self.configuration_file
        else:
            return self.configuration_file

    def get_configuration(self):
        load_dotenv(dotenv_path=self.configuration_file)
        env = {
            "AWS_ACCESS_KEY_ID" : os.getenv('AWS_ACCESS_KEY_ID'),
            "AWS_SECRET_ACCESS_KEY" : os.getenv('AWS_SECRET_ACCESS_KEY')
        }
        return env

    def add_defult_params(self):
        self.logger.info(f"Adding blank parameters for configuration.")
        AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID="
        AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY="
        with open(self.configuration_file,'w') as out:
            out.write('{}\n{}\n'.format(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY))

        return True

    def write_configuration(self, params):
        self.logger.info(f"Writing configuration to the file.")
        AWS_ACCESS_KEY_ID = f"AWS_ACCESS_KEY_ID={params['AWS_ACCESS_KEY_ID']}"
        AWS_SECRET_ACCESS_KEY = f"AWS_SECRET_ACCESS_KEY={params['AWS_SECRET_ACCESS_KEY']}"
        with open(self.configuration_file,'w') as out:
            out.write('{}\n{}\n'.format(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY))

        return True

    def is_configuration_done(self):
        configuration = self.get_configuration()
        if not configuration['AWS_ACCESS_KEY_ID'] or not configuration['AWS_SECRET_ACCESS_KEY']:
            return False
        return True




    
        