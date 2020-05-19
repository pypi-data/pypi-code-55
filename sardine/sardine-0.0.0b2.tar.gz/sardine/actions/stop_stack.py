import os

from sardine.actions.base import BaseAction
from sardine.config import DOCKER_COMPOSE_EXECUTABLE_PATH
from sardine.resolvers.manifest.local import LocalManifestResolver
from sardine.resolvers.repository.remote import RemoteRepositoryResolver


class StopStack(BaseAction):

    @classmethod
    def execute(cls, stack_name: str, *args, **kwargs):  # type: ignore
        manifest = LocalManifestResolver.load_manifest()
        repository_path = RemoteRepositoryResolver.get_repository_path(manifest[stack_name].repository_name)
        docker_compose_path = os.path.join(repository_path, manifest[stack_name].name, 'docker-compose.yml')
        os.system(f"{DOCKER_COMPOSE_EXECUTABLE_PATH} -f {docker_compose_path} down")
