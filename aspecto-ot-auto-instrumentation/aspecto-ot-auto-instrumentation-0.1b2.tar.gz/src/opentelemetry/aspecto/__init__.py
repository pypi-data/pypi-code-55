from opentelemetry import trace
from opentelemetry.ext.jaeger import JaegerSpanExporter
from opentelemetry.ext.zipkin import ZipkinSpanExporter
from opentelemetry.ext.otcollector.trace_exporter import (
    CollectorSpanExporter as OTSpanExporter,
)
from opentelemetry.sdk.trace import TracerProvider, Resource
from opentelemetry.sdk.trace.export import Span, SpanExporter
from requests import Response

import json
import uuid
import os
import socket
import sys
import subprocess
import typing
import threading

from opentelemetry.aspecto.utils import fetch_git_hash, read_aspecto_json
from opentelemetry.aspecto.config_service import get_config, get_config_http
from opentelemetry.aspecto.batch_processor import BatchExportSpanProcessor
from opentelemetry.aspecto.version import __version__

reqs = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
_INSTALLED_PACKAGES = [r.decode().split("==")[0] for r in reqs.split()]


def span_callback(span: Span, result: Response):
    try:
        request_body = result.request.body
        if request_body is not None and type(request_body) is str:
            span.set_attribute("http.request.body", request_body)

        if result.content is not None:
            span.set_attribute("http.response.body", result.content.decode("utf-8"))

        span.set_attribute(
            "http.request.headers", json.dumps(dict(result.request.headers))
        )
        span.set_attribute("http.response.headers", json.dumps(dict(result.headers)))
        span.set_attribute("aspecto.plugin.name", "requests")
    except Exception:
        pass


class AspectoInstrumentor:
    class DevJaegerPayload(typing.TypedDict):
        host: str
        port: int

    def __init__(
        self,
        service_name: str,
        aspecto_auth: str = None,
        dev_jaeger: DevJaegerPayload = None,
        env: str = "empty",
    ):
        if aspecto_auth is None:
            token_from_json = read_aspecto_json()
            if token_from_json is not None:
                aspecto_auth = token_from_json
            else:
                try:
                    aspecto_auth = os.environ["ASPECTO_AUTH"]
                except Exception:
                    raise ValueError(
                        "Must provide aspecto token via constructor or through ASPECTO_AUTH env var"
                    )

        if type(service_name) is not str:
            raise ValueError("Must provide str service_name")

        self.dev_jaeger = dev_jaeger
        self.service_name = service_name
        self.aspecto_auth = aspecto_auth
        self.resources = {
            "aspecto.version": __version__,
            "aspecto.instance.id": str(uuid.uuid4()),
            "aspecto.hostname": socket.gethostname(),
            "aspecto.token": aspecto_auth,
            "aspecto.githash": fetch_git_hash(),
            "aspecto.package.name": self.service_name,
            "aspecto.env": env,
            "telemetry.sdk.language": "python",
            "aspecto.runtime.version": sys.version,
        }
        self.span_processor = BatchExportSpanProcessor(tags=self.resources)
        self.__instrumented = False

    def instrument(self):
        trace_provider = TracerProvider(resource=Resource(labels=self.resources))
        trace.set_tracer_provider(trace_provider)

        if "Flask" in _INSTALLED_PACKAGES:
            print("Aspecto Instrumenting Flask")
            from opentelemetry.aspecto.ext.flask import FlaskInstrumentor

            FlaskInstrumentor().instrument()

        if "requests" in _INSTALLED_PACKAGES:
            print("Aspecto Instrumenting requests")
            from opentelemetry.ext.requests import RequestsInstrumentor

            RequestsInstrumentor().instrument(span_callback=span_callback)

        self.__instrumented = True
        trace.get_tracer_provider().add_span_processor(self.span_processor)

        threading.Thread(target=self.__initialize).start()

    def __initialize(self):
        try:
            config = get_config_http(self.aspecto_auth)
        except Exception as e:
            print("Failed initializing Aspecto: " + str(e))
            return

        print("Aspecto Initializing Privacy Engine")
        self.span_processor.init_privacy_engine(config["privacyRules"])

        # Jaeger dev
        if self.dev_jaeger is not None:
            dev_jaeger_exporter: SpanExporter = JaegerSpanExporter(
                service_name=self.service_name,
                agent_host_name=self.dev_jaeger["host"],
                agent_port=self.dev_jaeger["port"],
            )
            self.span_processor.add_exporter(dev_jaeger_exporter)

        # Zipkin
        zipkin_exporter: SpanExporter = ZipkinSpanExporter(
            service_name=self.service_name,
            host_name="jaeger-collector.aspecto.io",
            port=443,
            endpoint="/api/v2/spans",
            protocol="https",
        )
        self.span_processor.add_exporter(zipkin_exporter)

        # OTEL
        otel_collector_url = "opentelemetry-collector-opencensus.aspecto.io"
        if "collectorUrl" in config:
            otel_collector_url = config["collectorUrl"]

        collector_exporter: SpanExporter = OTSpanExporter(
            service_name=self.service_name, endpoint=otel_collector_url,
        )
        self.span_processor.add_exporter(collector_exporter)

    def uninstrument(self):
        if not self.__instrumented:
            return

        if "Flask" in _INSTALLED_PACKAGES:
            from opentelemetry.aspecto.ext.flask import FlaskInstrumentor

            FlaskInstrumentor().uninstrument()

        if "requests" in _INSTALLED_PACKAGES:
            print("Aspecto Instrumenting requests")
            from opentelemetry.ext.requests import RequestsInstrumentor

            RequestsInstrumentor().uninstrument()
