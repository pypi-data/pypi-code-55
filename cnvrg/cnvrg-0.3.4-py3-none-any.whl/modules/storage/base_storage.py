from cnvrg.modules.base_module import CnvrgBase
from cnvrg.helpers.apis_helper import download_file
from cnvrg.modules.cnvrg_files import CnvrgFiles
from cnvrg.modules import UnknownStsError
from cnvrg.helpers.crypto_helpers import decrypt
from typing import Dict, List
from botocore.exceptions import ClientError


class BaseStorage(CnvrgBase):
    def __init__(self, element: CnvrgFiles, working_dir: str, sts_path: str):
        self.element = element
        self.working_dir = working_dir
        self.init_sts(sts_path)
        self.conflicts = []

    def init_sts(self, sts_path):
        sts_file = download_file(sts_path, "/cnvrg/.cnvrg/.sts")
        if not sts_file:
            raise UnknownStsError("Cant find sts")
        with open(sts_file) as sts_content:
            if not sts_content:
                raise UnknownStsError("Cant find sts")
            self.key, self.iv, _ = sts_content.read().split("\n")

    def decrypt(self, text):
        return decrypt(self.key, self.iv, text)

    def decrypt_dict(self, props: Dict, keys: List = None):
        return {k: decrypt(self.key, self.iv, v) if k in keys else v for k,v in props.items()}

