import threading
import os
from typing import Optional, Callable, Iterable, Any, Mapping
from opentelemetry import context
# from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.django import DjangoInstrumentor
# from opentelemetry.instrumentation.urllib import URLLibInstrumentor
# from opentelemetry.instrumentation.redis import RedisInstrumentor
# from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
# from opentelemetry.instrumentation.pika import PikaInstrumentor

from opentelemetry import trace
#from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

import logging

old_thread = threading.Thread

class Threadv2(threading.Thread):
    def __init__(self, group: None = None, target: Optional[Callable[..., object]] = None, name: Optional[str] = None, args: Iterable[Any] = (), kwargs: Optional[Mapping[str, Any]]= None, *, daemon: Optional[bool] = None) -> None:
        self.opentelemetry_context = context.get_current()
        old_thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
    def run(self) -> None:
        if self.opentelemetry_context is not None:
            context.attach(self.opentelemetry_context)
        return super().run()


def patch_threading():
    threading.Thread = Threadv2

def setup_telemetry():
    resource = Resource(attributes={
            SERVICE_NAME: os.environ["OTEL_SERVICE_NAME"]
    })

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Psycopg2Instrumentor().instrument(enable_commenter=True, commenter_options={})
    DjangoInstrumentor().instrument()
    # URLLibInstrumentor().instrument()
    # RedisInstrumentor().instrument()
    # RequestsInstrumentor().instrument()
    URLLib3Instrumentor().instrument()
    # PikaInstrumentor().instrument()

    patch_threading()
