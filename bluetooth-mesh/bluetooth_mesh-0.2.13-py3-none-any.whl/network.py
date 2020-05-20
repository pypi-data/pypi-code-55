class Network:
    @property
    def network_keys(self):
        raise NotADirectoryError

    @property
    def application_keys(self):
        raise NotImplementedError

    @property
    def nodes(self):
        raise NotImplementedError

    @property
    def groups(self):
        raise NotImplementedError

    def get_node_group(self, node):
        raise NotImplementedError

    def get_group_address(self, group_name, model_class):
        raise NotImplementedError

    def get_node(self, *, uuid=None, address=None):
        raise NotImplementedError
