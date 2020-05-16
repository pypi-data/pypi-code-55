import importlib
from definitions import SERVER
from kaa import KaaServer


class Server:

    def get_server(self) -> KaaServer:
        spl = SERVER.split('.')
        class_name = spl[-1]
        module_name = '.'.join(spl[:-1])
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        return class_()

    def serve(self, env, start_response):
        server:KaaServer = self.get_server()
        return server.serve(env, start_response)
