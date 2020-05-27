
import pathlib
import shutil

import structlog

from .core.app import App
from .core.envs import Environment, get_images


logger = structlog.get_logger(__name__)


def from_env():
    """
    """
    return API()


class API:

    def __init__(self):
        self.apps = Apps()
        self.envs = Envs()

    def create(self, name):
        """
        Create

        Create a new application with the given name.
        """
        self.apps.create(name=name)

    def build(self, env="dev"):
        """
        Build

        Build the current application.
        """
        self.apps.build(env=env)


class Envs:
    """
    Envs API

    The envs API is used to manage environments.
    """

    def get(self, name):
        """
        Get environment with the given name.
        """
        return Environment(name)

    def list(self):
        """
        List environments.
        """
        images = get_images()
        return [Environment.from_image(img) for img in images]

    def create(self, name):
        """
        Create the given environment.

        If the environment exists locally, no action is taken.
        Otherwise, the environment is pulled from a remote
        repository (i.e. Docker Hub)
        """
        env = self.get(name)
        if not env.exists():
            env.init()

    def delete(self, name):
        """
        Delete environment with the given name.
        """
        env = self.get(name)
        if env.exists():
            env.delete()


class Apps:
    """
    App API

    The apps API is used to manage apps.
    """

    def create(self, name, dirname=None, runtime="python3.8"):
        """
        Create app

        Create new application with the given name in the given
        directory. if a directory isn't given, the current working
        directory will be used.
        """
        # Create root directory.
        dirname = pathlib.Path(dirname or pathlib.Path.cwd())
        root = dirname.joinpath(name)

        if root.exists():
            msg = f"App directory already exists: {root}"
            raise ValueError(msg)

        self._copy_template(root)

        app = App(root)
        app.init(runtime)

        return app

    def _copy_template(self, root):
        """
        Copy template

        Copy template files to the app directory.
        """
        template = pathlib.Path(__file__).parent.joinpath("template")
        shutil.copytree(template, root)

    def get(self, root=None):
        """
        Get app

        Get app from the given path. If a path isn't given, the
        current working directory will be used.
        """
        root = pathlib.Path(root or pathlib.Path.cwd())
        app = App(root)
        return app

    def build(self, root=None, env="dev"):
        """
        Build

        Build application at the given root. If no root is given,
        the current working directory is used.
        """
        app = self.get(root=root)
        app.build(env)

    def clean(self, root=None):
        """
        Clean

        Clean environments for the application at the given root. If
        no root is given, the current working directory is used.
        """
        app = self.get(root=root)
        app.clean()
        for env in app.envs:
            env.delete()


