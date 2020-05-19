import yaml


def read_yaml(path):
    with open(path) as file:
        docs = yaml.full_load(file)
    return docs


def write_yaml(file, data):
    with open(file, 'w') as file:
        yaml.dump(data, file)


class DockerSource:
    def __init__(self, path):
        self.path = path
        self.compose_file = read_yaml()

    def check_for_ports(self):
        print()

    def create_frame_work_directories(self):
        print()

    def create_docker_compose_file(self):
        print()

