import logging
import typing
from typing import Dict, Text

from RasaWSHH.cli.utils import print_warning
from RasaWSHH.constants import DOCS_BASE_URL
from RasaWSHH.core.lock_store import LockStore

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from RasaWSHH.core.agent import Agent


def run(
    model: Text,
    endpoints: Text,
    connector: Text = None,
    credentials: Text = None,
    **kwargs: Dict,
):
    """Runs a Rasa model.

    Args:
        model: Path to model archive.
        endpoints: Path to endpoints file.
        connector: Connector which should be use (overwrites `credentials`
        field).
        credentials: Path to channel credentials file.
        **kwargs: Additional arguments which are passed to
        `RasaWSHH.core.run.serve_application`.

    """
    import RasaWSHH.core.run
    import RasaWSHH.nlu.run
    from RasaWSHH.core.utils import AvailableEndpoints
    import RasaWSHH.utils.common as utils

    _endpoints = AvailableEndpoints.read_endpoints(endpoints)

    if not connector and not credentials:
        connector = "rest"
        print_warning(
            "No chat connector configured, falling back to the "
            "REST input channel. To connect your bot to another channel, "
            "read the docs here: {}/user-guide/"
            "messaging-and-voice-channels".format(DOCS_BASE_URL)
        )

    kwargs = utils.minimal_kwargs(kwargs, RasaWSHH.core.run.serve_application)
    RasaWSHH.core.run.serve_application(
        model,
        channel=connector,
        credentials=credentials,
        endpoints=_endpoints,
        **kwargs,
    )


def create_agent(model: Text, endpoints: Text = None) -> "Agent":
    from RasaWSHH.core.tracker_store import TrackerStore
    from RasaWSHH.core.utils import AvailableEndpoints
    from RasaWSHH.core.agent import Agent
    from RasaWSHH.core.brokers.broker import EventBroker

    _endpoints = AvailableEndpoints.read_endpoints(endpoints)

    _broker = EventBroker.create(_endpoints.event_broker)
    _tracker_store = TrackerStore.create(_endpoints.tracker_store, event_broker=_broker)
    _lock_store = LockStore.create(_endpoints.lock_store)

    return Agent.load(
        model,
        generator=_endpoints.nlg,
        tracker_store=_tracker_store,
        lock_store=_lock_store,
        action_endpoint=_endpoints.action,
    )
