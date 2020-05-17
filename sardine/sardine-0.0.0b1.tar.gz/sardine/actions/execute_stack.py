import os

from sardine.actions.base import BaseAction
from sardine.config import DOCKER_COMPOSE_EXECUTABLE_PATH
from sardine.resolvers.manifest.local import LocalManifestResolver
from sardine.resolvers.repository.remote import RemoteRepositoryResolver


class ExecuteStack(BaseAction):

    @classmethod
    def execute(cls, stack_name: str, *args, deattached: bool = False, **kwargs):
        manifest = LocalManifestResolver.load_manifest()
        repository_path = RemoteRepositoryResolver.get_repository_path(manifest[stack_name].repository_name)
        docker_compose_path = os.path.join(repository_path, manifest[stack_name].name, 'docker-compose.yml')
        command = f"{DOCKER_COMPOSE_EXECUTABLE_PATH} -f {docker_compose_path} up"
        if deattached:
            command += " -d"
        os.system(command)
