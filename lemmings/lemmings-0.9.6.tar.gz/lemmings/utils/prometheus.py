import gc
import logging
import os
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process

import psutil
from prometheus_client import generate_latest, REGISTRY, ProcessCollector, multiprocess, CollectorRegistry, Counter, Gauge

from lemmings.utils.influx import Influx

web_requests = Counter(f'web_requests', f'Latency for incoming web requests', ["url"])
class TestServer(BaseHTTPRequestHandler):
    def do_GET(self):
        web_requests.labels(url="/prometheus").inc()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(generate_latest(REGISTRY))

def run_server(server_class=HTTPServer, handler_class=TestServer):
    # reload(prometheus_client)
    multiprocess.MultiProcessCollector(REGISTRY)

    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("stop server")


ENV = 'prometheus_multiproc_dir'

def gauge(name, comment, fn):
    m = Gauge(name, comment, ["process", "process_group"])
    m.labels(os.getpid(), os.getppid()).set_function(fn)
    return m

def gauge_gen(name, comment, fn):
    m = Gauge(name, comment, ["generation", "process", "process_group"])
    for l in (0, 1, 2):
        m.labels(l, os.getpid(), os.getppid()).set_function(lambda: fn()[l])
    return m

def filter_stat(key):
    return lambda: [x[key] for x in gc.get_stats()]

class ProcessStat:
    def __init__(self):
        self.gc()
        self.mem()

        cpu = gauge('cpu_usage', 'Usage of the CPU in percent', lambda: psutil.cpu_percent(interval=1))
        disk = Gauge('used_disk_space', 'Used disk space in percent', ["partition", "process", "process_group"])
        for partition in psutil.disk_partitions():
            name = partition.mountpoint.replace('/', '_').replace('.', '_')
            disk.labels(name, os.getpid(), os.getppid()).set_function(lambda: psutil.disk_usage(partition.mountpoint).percent)

    def mem(self):
        def total():
            logging.warning(f"!!! {psutil.virtual_memory()}")
            return psutil.virtual_memory().total
        total = gauge('mem_total', 'Total reserver memory', total)
        available = gauge('mem_available', 'Free memory', lambda: psutil.virtual_memory().available)
        used = gauge('mem_used', 'Usage of memory', lambda: psutil.virtual_memory().used)
        percent = gauge('mem_usage', 'Usage of memory in percent', lambda: psutil.virtual_memory().percent)
        logging.warning(f"!!! INIT {psutil.virtual_memory()}")
        return psutil.virtual_memory().total

    def gc(self):
        enabled = gauge('mem_gc_enabled', 'Whether the garbage collector is enabled.', gc.isenabled)
        debug   = gauge('mem_gc_debug', 'The debug flags currently set on the Python GC.', gc.get_debug)
        count   = gauge_gen('mem_gc_count', 'Count of objects tracked by the Python garbage collector, by generation.', gc.get_count)
        threshold = gauge_gen('mem_gc_threshold', 'GC thresholds by generation', gc.get_threshold)
        total     = gauge_gen('mem_gc_collections_total', 'Number of GC collections that occurred by generation', filter_stat('collections'))
        collected = gauge_gen('mem_gc_collected_total', 'Number of garbage collected objects by generation', filter_stat('collected'))
        uncollect = gauge_gen('mem_gc_uncollectables', 'Number of uncollectable objects by generation', filter_stat('uncollectable'))

class Prometheus:
    def __init__(self, registry=REGISTRY,
                 include_process_info=False,
                 shared_dir='./build/prometheus.tmp'):

        if ENV in os.environ:
            self.path = os.environ.get(ENV)
        else:
            logging.info(f"no '{ENV}' in env, '{shared_dir}' will be used instead. smth can go wrong")
            self.path = os.environ.setdefault(ENV, shared_dir)
        shutil.rmtree(self.path, ignore_errors=True)
        os.mkdir(self.path)
        logging.info(f"Prometheus shared directory: {self.path}")

        if not registry:
            registry = CollectorRegistry()
        self.registry = registry
        multiprocess.MultiProcessCollector(self.registry)
        if include_process_info:
            ProcessCollector(registry=self.registry)
        self.influx = Influx(self.registry)
        self.args = []

    def filter(self, *args):
        self.args = args

    def dump_to_influx(self, all=False):
        args = self.args if not all else []
        return self.influx.save(*args)

    def clean(self):
        try:
            shutil.rmtree(self.path)
            logging.debug("temporary prometheus dir cleared")
            self.prom_server.terminate()
            logging.info("prometheus thread terminated")
            self.prom_server.join(5)
            logging.warning("prometheus thread stopped")

        except BaseException as e:
            logging.exception("problem with temporary prometheus dir: ")

    def start_server_process(self):
        self.prom_server = Process(name="PrometheusHttp", target=run_server, args=())
        self.prom_server.start()

