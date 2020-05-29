'''
    Using 'confused' for configuration management.
'''

class Configuration:
    def __init__(self):
        import confuse

        super().__init__()
        self.app_name = "cashiersync"
        self.config = confuse.LazyConfig(self.app_name, self.app_name)

    @property
    def ledger_working_dir(self):
        value = self.config["ledger_working_dir"].get()
        return value

    def save(self):
        ''' Saves the current config into the user's file '''
        import os
        import confuse

        content = self.config.dump()

        config_filename = os.path.join(self.config.config_dir(),
                                    confuse.CONFIG_FILENAME)
        with open(config_filename, 'w') as f:
            #yaml.dump(self.config, f)
            f.write(content)

        return True
