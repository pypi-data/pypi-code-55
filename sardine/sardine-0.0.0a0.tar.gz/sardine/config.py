import os

_user = os.path.expanduser("~")

SARDINE_FOLDER_PATH = os.getenv("SARDINE_FOLDER_PATH", os.path.join(_user, ".sardine"))

SARDINE_RC_PATH = os.getenv("SARDINE_RC_PATH", os.path.join(_user, ".config", "sardine", ".sardinerc"))
