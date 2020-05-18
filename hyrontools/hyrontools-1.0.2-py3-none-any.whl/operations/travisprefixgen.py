import os
from .operation import Operation
from ..errors import ValidationError


def _PASS(x): return "_".join(x.split("/"))


class TravisPrefixGeneration(Operation, register="travisprefixgen"):
    """
        Generates a deterministic key prefix from Travis metadata
    """
    HIDDEN = True
    SILENT = True

    ENVMAP = {
        "TRAVIS_COMMIT": ("commit", _PASS),
        "TRAVIS_REPO_SLUG": ("repo", _PASS),
        "TRAVIS_BRANCH": ("branch", _PASS),
        "TRAVIS_PULL_REQUEST": ("push", lambda x: x == "false")
    }

    @staticmethod
    def get_pull_request_sha():
        return os.environ.get("TRAVIS_PULL_REQUEST_SHA", None)

    @classmethod
    def get_pull_request(cls):
        retval = os.environ.get("TRAVIS_PULL_REQUEST", "false")
        if retval == "false":
            return None
        return retval

    def prevalidate(self, args):
        valid = True

        for envvar in self.ENVMAP.keys():
            if envvar not in os.environ:
                valid = False
                break

        if not valid or (self.get_pull_request()
                         and not self.get_pull_request_sha()):
            raise ValidationError(
                "Expected TravisCI variables missing!",
                False
            )

    def prepare_args(self, args):
        return {arg: xform(os.environ[envvar])
                for envvar, (arg, xform) in self.ENVMAP.items()}

    def run(self, commit: str, repo: str, branch: str, push: bool):
        prefix = f"travis/{repo}/{branch}"

        if push:
            prefix += f"/push/{commit}"
        else:
            prefix += f"/pull/{commit}/{self.get_pull_request()}/{self.get_pull_request_sha()}"  # noqa

        self.console.stream.write(prefix)
