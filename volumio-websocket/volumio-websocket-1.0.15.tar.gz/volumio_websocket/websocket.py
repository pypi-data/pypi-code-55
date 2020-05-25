
import socketio
import logging

_LOGGER = logging.getLogger(__name__)

# taken from https://github.com/volumio/Volumio2/blob/master/app/plugins/user_interface/websocket/index.js
_methods = {
    "getDeviceInfo": "pushDeviceInfo",
    "getState": "pushState",
    "getQueue": "pushQueue",
    "getMultiRoomDevices": "pushMultiRoomDevices",
    "getLibraryListing": "pushLibraryListing",
    "getMenuItems": "pushMenuItems",
    "getUiConfig": "pushUiConfig",
    "getBrowseSources": "pushBrowseSources",
    "browseLibrary": "pushBrowseLibrary",
    "search": "pushBrowseLibrary",
    "goTo": "pushBrowseLibrary",
    "GetTrackInfo": "pushGetTrackInfo",
    "addWebRadio": "pushAddWebRadio",
    "removeWebRadio": "pushBrowseLibrary",
    "getPlaylistContent": "pushPlaylistContent",
    "createPlaylist": "pushCreatePlaylist",
    "deletePlaylist": "pushListPlaylist",
    "listPlaylist": "pushListPlaylist",
    "addToPlaylist": "pushListPlaylist",
    "removeFromPlaylist": "pushBrowseLibrary",
    "playPlaylist": "pushPlayPlaylist",
    "enqueue": "pushEnqueue",
    "addToFavourites": "urifavourites",
    "removeFromFavourites": "pushBrowseLibrary",
    "playFavourites": "pushPlayFavourites",
    "addToRadioFavourites": "pushAddToRadioFavourites",
    "removeFromRadioFavourites": "pushRemoveFromRadioFavourites",
    "playRadioFavourites": "pushPlayRadioFavourites",
    "getSleep": "pushSleep"
    # TODO: There are lots more, continue at L673
}


class Websocket:
    def __init__(self, host, port, path=None):
        """Host, port and path must be all str."""
        self.host = host
        self.port = port
        self.path = path
        self.is_connected = False
        self._sio = None

    async def connect(self):
        url = f"http://{self.host}:{self.port}"

        if self.path is not None:
            if not str(self.path).startswith("/"):
                url += "/"
            url += str(self.path)

        self._sio = socketio.AsyncClient()
        await self._sio.connect(url)
        self.is_connected = True

    def get(self, name):
        return getattr(self, name, None)

    @classmethod
    def get_answer_name(cls, method):
        return _methods.get(method, None)

    async def call(self, method, params=None, wait=2):
        """
        Emit a method with params and returns the result.
        *wait* specifies, how long you want to wait for a result.
        This method makes the websocket a lot more like
        a request to an api endpoint.

        Returns None, if no result was present in the meanwhile.
        """

        name = self.get_answer_name(method)

        if name is not None:
            _LOGGER.debug("listen for event {}".format(name))

            @self._sio.on(name)
            def func(data):
                nonlocal name, self
                setattr(self, name, data)

        _LOGGER.debug("Emit event {} with params {}".format(method, params))
        await self._sio.emit(method, params)
        await self._sio.sleep(0.1)

        if name is None:
            return None

        counter = 0
        sleeptimer = 0.1

        data = self.get(name)
        while counter < wait and data is None:
            await self._sio.sleep(sleeptimer)
            counter += sleeptimer
            data = self.get(name)

        return data

    async def disconnect(self):
        await self._sio.disconnect()
        self.is_connected = False
