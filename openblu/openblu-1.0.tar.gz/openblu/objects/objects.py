"""This file contains the abstraction layers over the JSON response got from OpenBlu API"""


class ServerListing(object):
    """An abstraction layer over a dictionary object representing a server on the OpenBlu network.
       Server attributes can be accessed trough dot notation (e.g. ``foo.bar``) and trough slicing (``foo["bar"]``)

       :param data: The dictionary object converted from the JSON response from OpenBlu API
    """

    def __init__(self, data: dict):
        """Object constructor"""
        self._data = data

    def __getitem__(self, item):
        """Implements self['item']"""

        value = self._data.get(item, None)
        if not value:
            raise AttributeError(f"object of type '{type(self).__name__}' has no attribute '{item}'")
        return value

    def __getattr__(self, attr):
        """Implements self.attr"""

        return self.__getitem__(attr)

    def __repr__(self):
        """Implements repr(self)"""

        show = "\n"
        for index, (key, value) in enumerate(self._data.items()):
            show += f"{key}={value}"
            if index < len(self._data) - 1:
                show += ", \n"
        return f"ServerListing({show})"


class OpenVPN(ServerListing):

    def __init__(self, data):
        super().__init__(data)

    def __repr__(self):
        return f"<OpenVPN object at {hex(id(self))}>"


class Server(ServerListing):


    def __init__(self, data):
        """Object constructor"""

        super().__init__(data)
        self._data["openvpn"] = OpenVPN(self._data["openvpn"])

    def __repr__(self):
        """Implement repr(self)"""

        show = "\n"
        for index, (key, value) in enumerate(self._data.items()):
            show += f"{key}={value}"
            if index < len(self._data) - 1:
                show += ", \n"
        return f"Server({show})"

