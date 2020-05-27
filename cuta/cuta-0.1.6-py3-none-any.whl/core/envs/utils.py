
import functools
import shutil
import sys

import docker


@functools.lru_cache()
def get_docker():
    """
    Get docker client.
    """
    if not is_docker_installed():
        msg = "Docker is not installed!"
        raise RuntimeError(msg)

    if not is_docker_running():
        msg = "Docker is not currently running!"
        raise RuntimeError(msg)

    return docker.from_env()


def is_docker_installed():
    """
    Check if docker is installed

    Look for the `docker` executable. If it exists, docker is
    installed. Otherwise it isn't.
    """
    exe = shutil.which("docker")
    return bool(exe)


def is_docker_running():
    """
    Check if docker is running

    Use the docker client to get information about the docker
    daemon. If it throws an error, the daemon isn't running.
    """
    try:
        docker.from_env().info()
        return True
    except Exception:
        return False


def build_image(**kwargs):
    """
    Build image

    Build docker image using the given options.
    """
    client = docker.from_env()
    for item in client.api.build(**kwargs):
        error = item.get("errorDetail")
        if error:
            msg = f"Docker build failed!\nError:\n{error}"
            raise RuntimeError(msg)

        output = item.get("stream", "")
        output = output or item.get("aux", {}).get("ID")
        if output:
            yield output


def get_image(name):
    """
    Get docker image with the given name/id.
    """
    try:
        return get_docker().images.get(name)
    except docker.errors.ImageNotFound:
        return None


def get_images():
    """
    Get all docker images.
    """
    return get_docker().images.list(filters={"label": "io.cuta"})


def get_container(id_):
    """
    Get container with the given ID.
    """
    try:
        return get_docker().containers.get(id_)
    except docker.errors.NotFound:
        return None


def clear_lines(count=1):
    """
    Clear lines

    Clear the given number of lines from the console.
    """
    [sys.stdout.write("\x1b[1A\x1b[2K") for _ in range(count)]
