from sardine.exceptions.sardine_exception import SardineException


class ManifestNotFound(SardineException):

    def __init__(self, manifest_path: str):
        super().__init__(f"Sardine manifest not found. It should have been in '{manifest_path}'")
