"""Asynchronous Python client for SolarEnergy devices."""
import aiohttp
import asyncio
import async_timeout
from yarl import URL
from xml.parsers.expat import ExpatError
from typing import Any

from .__version__ import __version__
from .const import (
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
)
from .exceptions import (
    SolarEnergyError,
    SolarEnergyConnectionError,
    SolarEnergyTimeoutError,
    SolarEnergyClientError,
    SolarEnergyResponseError,
    SolarEnergyParseError,
    SolarEnergyContentTypeError,
    SolarEnergyAttributeError,
)
from .parser import parse_xml_to_json


class SolarEnergyInverter:
    """Main class for handling connections with SolarEnergy devices."""

    def __init__(
            self,
            host: str = None,
            port: int = DEFAULT_PORT,
            username: str = None,
            password: str = None,
            request_timeout: int = DEFAULT_TIMEOUT,
            session: aiohttp.ClientSession = None,
            tls: bool = False,
            verify_ssl: bool = False,
            user_agent: str = None,
    ) -> None:
        """Initialize connection with SolarEnergy device."""
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.request_timeout = request_timeout
        self._session = session
        self._close_session = False
        self.tls = tls
        self.verify_ssl = verify_ssl
        self.user_agent = user_agent

        if user_agent is None:
            self.user_agent = f"PythonSolarEnergy/{__version__}"

    async def _request(self, endpoint: str) -> aiohttp.ClientResponse:
        """Handle a request to an SolarEnergy device."""

        method = "GET"
        if self.host is None:
            url = URL.build(
                path=endpoint
            )
        else:
            scheme = "https" if self.tls else "http"
            url = URL.build(
                scheme=scheme, host=self.host, port=self.port, path=endpoint
            )

        auth = None
        if self.username and self.password:
            auth = aiohttp.BasicAuth(self.username, self.password)

        headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "text/xml",
            "Accept": "text/xml, text/plain, */*",
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    method,
                    url,
                    auth=auth,
                    headers=headers,
                    ssl=self.verify_ssl,
                    raise_for_status=True
                )
        except asyncio.TimeoutError as exc:
            raise SolarEnergyTimeoutError(
                "Timeout occurred while connecting to SolarEnergy inverter. Maybe it's on standby."
            ) from exc
        except (aiohttp.ClientError, RuntimeError) as exc:
            raise SolarEnergyClientError(
                "Error occurred while communicating with SolarEnergy inverter."
            ) from exc
        except NotImplementedError as exc:
            raise SolarEnergyConnectionError(
                "Unknown error occurred while communicating with SolarEnergy inverter."
            ) from exc

        return response

    async def _execute(
            self,
            endpoint: str,
            root_element: str = None
    ) -> Any:
        """Send a request message to the SolarEnergy device."""
        # Todo: return_type: xml, dict, etc
        content_type = "text/xml"
        response = await self._request(endpoint)
        try:
            data = await response.json(
                loads=parse_xml_to_json, content_type=content_type
            )
            return data if root_element is None else data[root_element]

        except ExpatError as exc:
            raise SolarEnergyParseError(
                "Received malformed xml from inverter."
            ) from exc
        except aiohttp.ContentTypeError as exc:
            raise SolarEnergyContentTypeError(
                "Received unexpected mime type from inverter."
            ) from exc
        except (KeyError, TypeError) as exc:
            raise SolarEnergyAttributeError(
                "Received invalid data from inverter."
            ) from exc
        except NotImplementedError as exc:
            raise SolarEnergyResponseError(
                "Unknown error occurred with response of SolarEnergy inverter."
            ) from exc

    async def get_info(self) -> Any:
        return await self._execute(
            endpoint="/equipment_data.xml",
            root_element="equipment_data"
        )

    async def get_data(self) -> Any:
        return await self._execute(
            endpoint="/real_time_data.xml",
            root_element="real_time_data"
        )

    async def get_network(self) -> Any:
        return await self._execute(
            endpoint="/network_data.xml",
            root_element="network_data"
        )

    async def close_session(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "SolarEnergyInverter":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close_session()
