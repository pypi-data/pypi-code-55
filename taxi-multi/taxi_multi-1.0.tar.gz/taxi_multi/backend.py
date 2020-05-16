from collections import defaultdict

from taxi.backends import BaseBackend
from taxi.plugins import plugins_registry

class MultiBackend(BaseBackend):
    def __init__(self, **kwargs):
        super(MultiBackend, self).__init__(**kwargs)
        self.settings = self.context['settings']

        self.backends = []
        for backend_name in kwargs['options']['backends'].split(','):
            backend = plugins_registry._load_backend(self.get_backend_uri(backend_name), self.context)
            self.backends.append(backend)

    def get_backend_uri(self, backend_name):
        for backend, uri in self.settings.config.items('multi'):
            if backend == backend_name:
                return uri

        raise Exception(f'Cannot find backend {backend_name} in [multi]')

    def push_entry(self, date, entry):
        for backend in self.backends:
            backend.push_entry(date, entry)

    def post_push_entries(self):
        for backend in self.backends:
            backend.post_push_entries()

    def get_projects(self):
        projects = []
        for backend in self.backends:
            projects += backend.get_projects()

        return projects
