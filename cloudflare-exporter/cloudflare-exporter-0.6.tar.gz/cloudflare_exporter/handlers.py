from aiohttp import web

from prometheus_client import generate_latest
from prometheus_client.core import REGISTRY


def metric_to_text():
    return generate_latest(REGISTRY).decode('utf-8')


async def handle_metrics(_request):
    return web.Response(text=metric_to_text())


async def handle_health(_request):
    health_text = 'ok'
    health_status = 200
    return web.Response(status=health_status, text=health_text)
