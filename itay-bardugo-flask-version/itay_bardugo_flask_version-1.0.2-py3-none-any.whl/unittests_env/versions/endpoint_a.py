from unittests_env import make_app
from flask_version.utils import support_version


@support_version("1.0")
def version_a():
    return "i am an endpoint for version 1.0"
