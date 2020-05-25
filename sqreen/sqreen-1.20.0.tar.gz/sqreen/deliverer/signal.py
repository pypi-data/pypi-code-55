# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Signal delivery method
"""
import logging

from .._vendors.sqreen_security_signal_sdk import Client
from .._vendors.sqreen_security_signal_sdk.sender import Sender
from ..config import CONFIG
from ..events import RequestRecord
from ..http_client import USER_AGENT
from ..remote_exception import RemoteException
from .simple import SimpleDeliverer

LOGGER = logging.getLogger(__name__)


class AgentSignalSender(Sender):

    default_base_url = CONFIG["INGESTION_URL"]


class AgentSignalClient(Client):

    sender_class = AgentSignalSender
    user_agent = USER_AGENT


class SignalDeliverer(SimpleDeliverer):

    client_cls = AgentSignalClient

    def __init__(self, session, batch_size, max_staleness):
        super(SignalDeliverer, self).__init__(session)
        self.batch_size = batch_size
        self.original_max_staleness = max_staleness
        self.max_staleness = max_staleness
        self.client = self.client_cls(
            token=session.session_token,
            max_batch_size=self.batch_size,
            interval_batch=self.max_staleness,
            session_token=True,
            proxy_url=CONFIG["PROXY_URL"],
        )

    def post_event(self, event):
        if isinstance(event, RequestRecord):
            return self.client.trace(**event.to_trace())
        elif isinstance(event, RemoteException):
            return self.client.signal(**event.to_signal())
        LOGGER.debug("Event not supported: %r", event)
        raise NotImplementedError

    def post_metrics(self, metrics):
        for metric in metrics:
            payload = {
                "capture_interval_s": metric["period"],
                "date_started": metric["start"],
                "date_ended": metric["finish"],
            }
            if metric["kind"] == "Binning":
                payload_schema = "metric_binning/2020-01-01T00:00:00.000Z"
                o = metric["observation"]
                payload.update({
                    "unit": o["u"],
                    "base": o["b"],
                    "bins": o["v"],
                    "max": o["v"].pop("max"),
                })
            else:
                payload_schema = "metric/2020-01-01T00:00:00.000Z"
                payload.update({
                    "kind": metric["kind"].lower(),
                    "values": [{"key": str(k), "value": v}
                               for k, v in metric["observation"].items()],
                })

            self.client.metric(
                "sq.agent.metric.{}".format(metric["name"]),
                payload,
                payload_schema=payload_schema,
                source="sqreen:agent:python",
            )

    def drain(self, resiliently):
        self.client.flush()

    def tick(self):
        self.client.flush(soft=True)
