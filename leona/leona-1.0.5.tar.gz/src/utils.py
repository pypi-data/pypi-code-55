import os
import yaml

DEFAULT_CONFIG_PATH = os.path.join(os.getcwd(), "static/CONFIG_TEMPLATE.yml")
OUT_FILE_PATH = os.path.join(os.path.expanduser("~"), "leona_config.yml")

def get_config():
    if (os.path.exists(OUT_FILE_PATH) == False):
        create_config()
        config_file_path = os.path.join(os.path.expanduser("~"), "leona_config.yml")
        with open(config_file_path) as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
        return config
    else:
        config_file_path = os.path.join(os.path.expanduser("~"), "leona_config.yml")
        with open(config_file_path) as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
        return config
  
def create_config():
    with open(DEFAULT_CONFIG_PATH) as default_config:
        config = yaml.load(default_config, Loader=yaml.FullLoader)
        output_file = yaml.dump(config)
        with open(OUT_FILE_PATH, "w") as final_config:
            final_config.write(output_file)