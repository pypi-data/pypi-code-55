from tracing.local_context import LocalContext

DefaultContext = LocalContext(service="Patent Classifer", span_id=0)

import atexit
atexit.register(DefaultContext.flush_buffer_to_agent)
