
import asyncio
import socketio

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

    async def connect(self):
        url = f"http://{self.host}:{self.port}"

        if self.path is not None:
            if not str(self.path).startswith("/"):
                url += "/"
            url += str(self.path)

        self._sio = socketio.AsyncClient()
        await self._sio.connect(url)
        self.is_connected = True

    async def emit(self, method, params=None):
        """
        Emit a method with params.

        Returns a  *name* in this object,
        where you can find your results.
        Use obj.get(*name*) to get the results.
        """
        if method in _methods:
            state_name = self.get_answer_name(method)

            @self._sio.on(state_name)
            def func(data):
                nonlocal state_name, self
                setattr(self, state_name, data)
        else:
            state_name = None

        await self._sio.emit(method, params)
        await self._sio.sleep(0.1)

        return state_name

    def get(self, name):
        return getattr(self, name, None)

    @classmethod
    def get_answer_name(cls, method):
        return _methods[method]

    async def command(self, command):
        """Emit a call without any params."""
        await self.emit(command)

    async def call(self, method, params=None, wait=2):
        """
        Emit a method with params and returns the result.
        *wait* specifies, how long you want to wait for a result.
        This method makes the websocket a lot more like
        a request to an api endpoint.

        Returns None, if no result was present in the meanwhile.
        """

        name = await self.emit(method, params)
        if name is None:
            return None

        counter = 0
        sleeptimer = 0.1

        data = self.get(name)
        while counter < wait and data is None:
            asyncio.sleep(sleeptimer)
            counter += sleeptimer
            data = self.get(name)

        return self.get(name)

    async def disconnect(self):
        await self._sio.disconnect()
        self.is_connected = False
