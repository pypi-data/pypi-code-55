class VersionSearcherResult(object):

    def __init__(self, current_version, previous_version):
        self.current_version = current_version
        self.previous_version = previous_version if previous_version else None

        if not current_version:
            raise Exception(
                "No value found for current version"
            )