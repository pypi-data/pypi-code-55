class Environment:

    def __init__(self, n, u, ns):
        self.name = n
        self.url = u
        self.namespace = ns
        self.deployments = []