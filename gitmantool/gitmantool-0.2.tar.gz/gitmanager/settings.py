import yaml
import os
import sys

# ─── SETTINGS CLASS ─────────────────────────────────────────────────────────────

class SettingsFile:
    NAME = "settings.gm"
    

    def create(self):
        print("Settings file not exist, creating...")
        link = input("Input link of git server: ")
        with open(self.NAME, 'w') as f: 
            yaml.dump({ "link": link }, f, default_flow_style=False)

    @property
    def link(self):
        try:
            with open(self.NAME, "r") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(f"error: {e}")
            sys.exit()
        else:
            return data['link']
    
    @property
    def exist(self):
        return os.path.isfile(self.NAME)

    @property
    def server(self):
        return self.link.split("/")[2]
    
    @property
    def username(self):
        return self.link.split("/")[3]
    
    @property
    def repo(self):
        return self.link.split("/")[4]


# ────────────────────────────────────────────────────────────────────────────────


# ─── CREDENTIALS MANAGER ────────────────────────────────────────────────────────

class CredsManager:

    def __init__(self):
        self.creds_folder = os.environ["HOME"] + "/.gitmanager/"
        self.creds_file = "creds.yaml"
        self.creds_full_path = self.creds_folder + self.creds_file
        if not self.exist:
            sys.exit("El archivo de credeciales no existe")
    
    @property
    def exist(self):
        return os.path.isfile(self.creds_full_path)

    def get_token(self, server):
        try:
            with open(self.creds_full_path, "r") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            sys.exit("error al leer creds")
        else:
            if data[server] is None:
                sys.exit("Token no configurado")
            return data[server]