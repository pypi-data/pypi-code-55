from collections import namedtuple

DEFAULT_AGENT_URL = "http://127.0.0.1:8000/api/traces"
DEFAULT_REQUEST_BUFFER_SIZE = 40

SPAN_RECORD = namedtuple(
    "SpanRecord",
    "parent_id, span_id, start_time, trace_id, service, operation, end_time, children, meta",
)


def convert_span_record_to_key_value(span_record: SPAN_RECORD):
    """
    This is a separate function only so we can modify this code if asdict() is deprecated.
    :param span_record:
    :return:
    """
    return span_record._asdict()
