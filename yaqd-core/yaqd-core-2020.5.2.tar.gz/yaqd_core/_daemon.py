#! /usr/bin/env python3

__all__ = ["Base"]

import argparse
import asyncio
import functools
import inspect
import logging as logging_
import pathlib
import signal
import sys
import time
from typing import Dict, List, Optional, Any, Union, Sequence, Set

import appdirs  # type: ignore
import msgpack  # type: ignore
import toml

from .__version__ import __version__, __rpc_version__
from . import logging
from . import msgpack  # type: ignore
from .exceptions import InvalidRequest, MethodNotFound

logger = logging.getLogger("yaqd_core")


class Base:
    defaults: Dict[str, Any] = {}
    traits: List[str] = ["is-daemon"]
    _kind: str = "base"
    _version: Optional[str] = None  # this class should not be directly instantiated
    _daemons: List["Base"] = []

    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        """Create a yaq daemon.

        Parameters
        ----------
        name: str
            A name for this daemon
        config: dict
            Configuration parameters
        config_filepath: str
            The path for the configuration (not used internally, availble to clients)
        """
        self.name = name
        self.kind = self.__class__._kind
        self.config = config
        self._config_filepath = config_filepath
        self._state_filepath = (
            pathlib.Path(appdirs.user_data_dir("yaqd-state", "yaq"))
            / self.kind
            / f"{self.name}-state.toml"
        )
        self.logger = logging.getLogger(self.name)
        if "log_level" in self.config:
            self.logger.setLevel(logging.name_to_level[self.config["log_level"]])
        if self.config.get("log_to_file"):
            fh = logging_.FileHandler(
                self._state_filepath.with_name(
                    f"{self.name}-{time.strftime('%Y-%m-%dT%H:%M:%S%z')}.log"
                )
            )
            fh.setFormatter(logging.formatter)
            self.logger.addHandler(fh)
        self.logger.info(f"Config File Path = {self._config_filepath}")
        self.logger.info(f"State File Path = {self._state_filepath}")
        self.logger.info(f"TCP Port = {config['port']}")
        self._clients: List[str] = []

        self.serial = config.get("serial", None)
        self.make = config.get("make", None)
        self.model = config.get("model", None)

        self._busy_sig = asyncio.Event()
        self._not_busy_sig = asyncio.Event()

        self._loop = asyncio.get_event_loop()

        try:
            self._state_filepath.parent.mkdir(parents=True, exist_ok=True)
            with self._state_filepath.open("rt") as f:
                state = toml.load(f)
        except (toml.TomlDecodeError, FileNotFoundError):
            state = {}

        self._load_state(state)
        self._tasks = [
            self._loop.create_task(self.save_state()),
            self._loop.create_task(self.update_state()),
        ]

    @classmethod
    def main(cls):
        """Run the event loop."""
        loop = asyncio.get_event_loop()
        if sys.platform.startswith("win"):
            signals = ()
        else:
            signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
        for s in signals:
            loop.add_signal_handler(
                s, lambda s=s: asyncio.create_task(cls.shutdown_all(s, loop))
            )

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--config",
            "-c",
            default=(
                pathlib.Path(appdirs.user_config_dir("yaqd", "yaq"))
                / cls._kind
                / "config.toml"
            ),
            action="store",
            help="Path to the configuration toml file.",
        )
        parser.add_argument(
            "--verbose",
            "-v",
            action="store_const",
            dest="log_level",
            const="debug",
            help="Alias for --log-level=debug",
        )
        parser.add_argument(
            "--log-level",
            "-l",
            action="store",
            dest="log_level",
            choices=[
                "debug",
                "info",
                "notice",
                "warning",
                "error",
                "critical",
                "alert",
                "emergency",
            ],
            help="Set the log level explicitly",
        )

        parser.add_argument("--version", action="store_true")

        args = parser.parse_args()

        if args.log_level:
            logging.setLevel(logging.name_to_level[args.log_level])

        if args.version:
            print(f"'{cls._kind}' version {cls._version}")
            print(f"yaq rpc version {__rpc_version__}")
            print(f"yaqd_core version {__version__}")
            print(f"Python {sys.version}")
            sys.exit(0)

        config_filepath = pathlib.Path(args.config)
        config_file = toml.load(config_filepath)

        main_task = loop.create_task(cls._main(config_filepath, config_file, args))
        try:
            loop.run_forever()
        except asyncio.exceptions.CancelledError:
            pass
        finally:
            loop.close()

    @classmethod
    async def _main(cls, config_filepath, config_file, args=None):
        """Parse command line arguments, start event loop tasks."""
        loop = asyncio.get_running_loop()
        cls.__servers = []
        for section in config_file:
            try:
                config = cls._parse_config(config_file, section, args)
            except ValueError:
                pass
            await cls._start_daemon(section, config, config_filepath)

        while cls.__servers:
            awaiting = cls.__servers
            cls.__servers = []
            await asyncio.wait(awaiting)
            await asyncio.sleep(1)
        loop.stop()

    @classmethod
    async def _start_daemon(cls, name, config, config_filepath):
        loop = asyncio.get_running_loop()
        daemon = cls(name, config, config_filepath)
        cls._daemons.append(daemon)

        # This function is here to namespace `daemon` so it doesn't
        # get overridden for the lambda
        def server(daemon):
            return lambda: Protocol(daemon)

        ser = await loop.create_server(
            server(daemon), config.get("host", ""), config.get("port", None)
        )
        daemon._server = ser
        cls.__servers.append(ser.serve_forever())

    @classmethod
    def _parse_config(cls, config_file, section, args=None):
        if section == "shared-settings":
            raise ValueError(f"Section name '{section}' reserved")
        config = {}
        for c in reversed(cls.mro()):
            try:
                config.update(c.defaults)
            except AttributeError:
                continue
        config.update(config_file.get("shared-settings", {}).copy())
        config.update(config_file[section])
        if args:
            try:
                if args.log_level:
                    config.update(log_level=args.log_level)
            except AttributeError:
                pass

        if not config.get("enable", True):
            logger.info(f"Section '{section}' is disabled")
            raise ValueError(f"Section '{section}' is disabled")
        return config

    @classmethod
    async def shutdown_all(cls, sig, loop):
        """Gracefully shutdown the asyncio loop.

        Gathers all current tasks, and allows daemons to perform cleanup tasks.

        Adapted from https://www.roguelynn.com/words/asyncio-graceful-shutdowns/
        Original code is licensed under the MIT license, and sublicensed here.
        """
        logger.info(f"Received signal {sig.name}...")
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        logger.info(f"Cancelling {len(tasks)} outstanding tasks")
        logger.debug(f"{[task.get_name() for task in tasks]}")
        [task.cancel() for task in tasks]
        # This is done after cancelling so that shutdown tasks which require the loop
        # are not themselves cancelled.
        [d.close() for d in cls._daemons]
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        await asyncio.gather(*tasks, return_exceptions=True)
        [d._save_state() for d in cls._daemons]
        if hasattr(signal, "SIGHUP") and sig == signal.SIGHUP:
            config_filepath = [d._config_filepath for d in cls._daemons][0]
            config_file = toml.load(config_filepath)
            await cls._main(config_filepath, config_file)
        loop.stop()

    def shutdown(self, restart=False):
        self.logger.info(f"Shutting Down {self.name}")
        self.logger.info(f"Cancelling {len(self._tasks)} outstanding tasks")
        self.logger.debug(f"{[task.get_name() for task in self._tasks]}")
        [task.cancel() for task in self._tasks]
        self.close()
        self._server.close()
        if restart:
            config_filepath = self._config_filepath
            config_file = toml.load(config_filepath)
            try:
                config = type(self)._parse_config(config_file, self.name)
                self._loop.create_task(
                    type(self)._start_daemon(self.name, config, config_filepath)
                )
            except ValueError as e:
                self.logger.error(e.message)

    def _connection_made(self, peername: str) -> None:
        self._clients.append(peername)
        self.logger.debug(f"_connection_made {self._clients}")

    def _connection_lost(self, peername: str) -> None:
        self._clients.remove(peername)
        self.logger.debug(f"_connection_lost {self._clients}")

    def get_traits(self) -> List[str]:
        """Get list of yaq-daemon traits."""
        implemented_traits: Set[str] = set()
        for ty in type(self).mro():
            if issubclass(ty, Base):
                implemented_traits |= set(ty.traits)
        return list(implemented_traits)

    def get_version(self) -> Optional[str]:
        """Get version."""
        return self._version

    def _save_state(self) -> None:
        """Write the current state to disk."""
        with open(self._state_filepath, "wt") as f:
            toml.dump(self.get_state(), f)

    async def save_state(self):
        """Schedule writing the current state to disk.

        Note: Current implementation only writes while busy (and once after busy)
        """
        while True:
            while self._busy:
                self._save_state()
                await asyncio.sleep(0.1)
            self._save_state()
            await self._busy_sig.wait()

    def get_config_filepath(self) -> str:
        """Retrieve the current filepath of the configuration."""
        return str(self._config_filepath.absolute())

    def get_config(self) -> Dict[str, Any]:
        """Retrieve the current configuration, including any defaults."""
        return self.config

    def list_methods(self) -> List[str]:
        """Return a list of all public methods."""
        filt = filter(lambda x: x[0] != "_", dir(self.__class__))
        # Use `isfunction` on the `__class__` to filter out classmethods
        filt = filter(lambda x: inspect.isfunction(getattr(self.__class__, x)), filt)
        filt = filter(lambda x: not asyncio.iscoroutinefunction(getattr(self, x)), filt)
        return list(filt)

    def set_state(self, **kwargs) -> None:
        """Set the daemon state.

        Input may be any portion of the entire state dictionary.
        Key value pairs that are not defined are propagated from the current daemon state.
        If input is not valid, daemon will raise exception.

        Parameters
        ----------
        state: dict
            New state
        """
        full = self.get_state()
        full.update(kwargs)
        self._load_state(full)
        self._save_state()

    def help(self, method: Optional[Union[str, Sequence[str]]] = None):
        """Return useful, human readable information about methods.

        Parameters
        ----------
        method: str or list of str (optional)
            The method or list of methods for which help is requested.
            Default is information on the daemon itself.

        Returns
        -------
        str or list of str: The requested documentation.
        """
        if method is None:
            return self.__doc__
        if isinstance(method, str):
            fun = getattr(self, method)
            return f"{method}{str(inspect.signature(fun))}\n{fun.__doc__}"
        return list(self.help(c) for c in method)

    def id(self) -> Dict[str, Optional[str]]:
        """Dictionary of identifying information for the daemon."""
        return {
            "name": self.name,
            "kind": self.kind,
            "make": self.make,
            "model": self.model,
            "serial": self.serial,
        }

    @property
    def _busy(self) -> bool:
        """Indicates the current 'busy' state for use in internal functions.

        Setting busy can be done with `self._busy = <True|False>`.
        Async tasks can wait for either sense using `await self._[not_]busy_sig.wait()`.
        """
        return self._busy_sig.is_set()

    @_busy.setter
    def _busy(self, value):
        if value:
            self._busy_sig.set()
            self._not_busy_sig.clear()
        else:
            self._not_busy_sig.set()
            self._busy_sig.clear()

    def busy(self) -> bool:
        """Boolean representing if the daemon is busy (state updated) or not."""
        return self._busy

    # The following functions (plus __init__) are what most daemon need to implement

    async def update_state(self):
        """Continually monitor and update the current daemon state."""
        pass

    def get_state(self) -> Dict[str, Any]:
        """Return the current daemon state."""
        return {}

    def _load_state(self, state):
        """Load an initial state from a dictionary (typically read from the state.toml file).

        Must be tolerant of missing fields, including entirely empty initial states.
        Raise an exception if state is invalid.

        Parameters
        ----------
        state: dict
            The saved state to load.
        """
        pass

    def close(self):
        """Perform necessary clean-up and stop running."""
        pass


class Protocol(asyncio.Protocol):
    def __init__(self, daemon, *args, **kwargs):
        self._daemon = daemon
        self.logger = daemon.logger
        self._method_list = self._daemon.list_methods()
        asyncio.Protocol.__init__(self, *args, **kwargs)
        self._error_codes = {
            msgpack.exceptions.UnpackException: {
                "code": -32700,
                "message": "Parse error",
            },
            InvalidRequest: {"code": -32600, "message": "Invalid Request"},
            MethodNotFound: {"code": -32601, "message": "Method not found"},
            TypeError: {"code": -32602, "message": "Invalid params"},
        }

    def connection_lost(self, exc):
        peername = self.transport.get_extra_info("peername")
        self.logger.info(f"Connection lost from {peername} to {self._daemon.name}")
        self._daemon._connection_lost(peername)

    def connection_made(self, transport):
        """Process an incomming connection."""
        peername = transport.get_extra_info("peername")
        self.logger.info(f"Connection made from {peername} to {self._daemon.name}")
        self.transport = transport
        self._daemon._connection_made(peername)

    def data_received(self, data):
        """Process an incomming request."""
        self.logger.info(f"Data received: {repr(data)}")
        if not self._daemon._server.is_serving():
            self.transport.close()
        unpacker = msgpack.Unpacker()
        unpacker.feed(data)
        try:
            for o in unpacker:
                self.run_method(o)
        except (msgpack.exceptions.UnpackException, ValueError):
            # Handle invalid msgpack
            response = {
                "ver": "1.0",
                "error": self._error_codes[msgpack.exceptions.UnpackException],
                "id": None,
            }
            self.transport.write(msgpack.packb(response))

    def run_method(self, request):
        response = {"ver": "1.0"}
        # Ignoring "ver" in request
        notification = False
        shutdown = False
        try:
            if not isinstance(request, dict) or "method" not in request:
                request = {}
                raise InvalidRequest
            shutdown = request.get("method") == "shutdown"
            notification = "id" not in request

            method = request["method"]
            response["id"] = request.get("id")
            params = request.get("params", [])

            if not isinstance(method, str):
                notification = False
                raise InvalidRequest
            if method not in self._method_list:
                raise MethodNotFound(method)
            fun = getattr(self._daemon, method)
            if isinstance(params, list):
                response["result"] = fun(*params)
            else:
                response["result"] = fun(**params)
        except BaseException as e:
            self.logger.error(
                f"Caught exception in {request.get('method', 'RPC')}: {repr(e)}"
            )
            if type(e) in self._error_codes:
                response["error"] = self._error_codes[type(e)]
            else:
                response["error"] = {"code": -1, "message": repr(e)}
        if "error" in response:
            response.pop("result", None)
            try:
                response["id"] = request.get("id", None)
            except:
                response["id"] = None
        # Notifications get no response
        if response and not notification:
            self.transport.write(msgpack.packb(response))
        if shutdown:
            self.transport.close()


if __name__ == "__main__":
    Base.main()
