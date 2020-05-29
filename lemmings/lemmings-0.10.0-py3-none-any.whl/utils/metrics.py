import inspect
import functools
import time
from timeit import default_timer

from prometheus_client import Counter, Histogram, Gauge, Summary
from quart import request

from lemmings.utils.timer_prom import QuantileSummary


def calc_value(f):
    if not callable(f):
        return lambda x: f
    if inspect.getfullargspec(f).args:
        return lambda x: f(x)
    else:
        return lambda x: f()


class BasePrometheusMetrics(object):
    def __init__(self, app, registry=None):
        self.app = app
        if registry:
            self.registry = registry
        else:
            from prometheus_client import REGISTRY as DEFAULT_REGISTRY
            self.registry = DEFAULT_REGISTRY

    def summary(self, name, description, labels=None, **kwargs):
        return self._track(
            Summary,
            lambda metric, time: metric.observe(time),
            kwargs, name, description, labels
        )

    def gauge(self, name, description, labels=None, **kwargs):
        return self._track(
            Gauge,
            lambda metric, time: metric.dec(),
            kwargs, name, description, labels,
            before=lambda metric: metric.inc()
        )

    def counter(self, name, description, labels=None, **kwargs):
        return self._track(
            Counter,
            lambda metric, time: metric.inc(),
            kwargs, name, description, labels
        )

    def _track(self, metric_type, metric_call, metric_kwargs, name, description, labels, before=None):
        """
        Internal method decorator logic.

        :param metric_type: the type of the metric from the `prometheus_client` library
        :param metric_call: the invocation to execute as a callable with `(metric, time)`
        :param metric_kwargs: additional keyword arguments for creating the metric
        :param name: the name of the metric
        :param description: the description of the metric
        :param labels: a dictionary of `{labelname: callable_or_value}` for labels
        :param before: an optional callable to invoke before executing the
            request handler method accepting the single `metric` argument
        """

        if labels is not None and not isinstance(labels, dict):
            raise TypeError('labels needs to be a dictionary of {labelname: callable}')
        label_names = labels.keys() if labels else tuple()

        label_generator = tuple((key, calc_value(call)) for key, call in labels.items()) if labels else tuple()

        parent_metric = metric_type(
            name, description, labelnames=label_names, registry=self.registry,
            **metric_kwargs
        )

        def get_metric(result):
            if label_names:
                return parent_metric.labels(**{key: call(result) for key, call in label_generator})
            else:
                return parent_metric

        def decorator(f):
            @functools.wraps(f)
            async def func(*args, **kwargs):
                metric = None
                if before:
                    metric = get_metric(None)
                    before(metric)

                start_time = default_timer()
                try:
                    result = await f(*args, **kwargs)
                    if not metric:
                        metric = get_metric(result)
                    total_time = max(default_timer() - start_time, 0)
                    metric_call(metric, time=total_time)
                    return result
                except Exception as ex:
                    raise ex
            return func
        return decorator


class PrometheusMetrics(BasePrometheusMetrics):
    """
    The default metrics include a Histogram for HTTP request latencies
    and number of HTTP requests plus a Counter for the total number
    of HTTP requests.

        @app.route('/<item_type>')
        @metrics.counter('invocation_by_type', 'Number of invocations by type', labels={'item_type': lambda: request.view_args['type']})
        def by_type(item_type):
            pass  # only the counter is collected, not the default metrics

        @app.route('/long-running')
        @metrics.gauge('in_progress', 'Long running requests in progress')
        def long_running():
            pass

        @app.route('/status/<int:status>')
        @metrics.summary('requests_by_status', 'Request latencies by status', labels={'status': lambda r: r.status_code})
        @metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path',
                           labels={'status': lambda r: r.status_code, 'path': lambda: request.path})
        def echo_status(status):
            return 'Status: %s' % status, status

    Label values can be defined as callables:
        - With a single argument that will be the Response object
        - Without an argument, possibly to use with the `request` object
    """

    def __init__(self, app, registry=None):
        super(PrometheusMetrics, self).__init__(app, registry)

        # latency = Summary('http_request_duration_seconds', 'HTTP request duration in seconds',
        #                   ('method', 'path', 'status'), registry=self.registry)
        latency = QuantileSummary('http_request_duration_seconds', 'HTTP request duration in seconds',
                          ('method', 'path', 'status'), registry=self.registry)

        def before_request():
            request.prom_start_time = time.perf_counter()
        def after_request(response):
            if hasattr(request, 'prom_start_time'):
                request.prom_end_time = time.perf_counter()
                total_time = max(time.perf_counter() - request.prom_start_time, 0)
                latency.labels(request.method, request.path, response.status_code).observe(total_time)
            return response
        def teardown_request(exception=None):
            if hasattr(request, 'prom_start_time'):
                total_time = max(time.perf_counter() - request.prom_start_time, 0)
                if not hasattr(request, 'prom_end_time'):
                    latency.labels(request.method, request.path, 500).observe(total_time)
            return
        app.before_request(before_request)
        app.after_request(after_request)
        app.teardown_request(teardown_request)


