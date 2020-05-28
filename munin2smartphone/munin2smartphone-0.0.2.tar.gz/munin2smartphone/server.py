import aiohttp.web

import quicklogging

from . import widget


class Server:
    def __init__(self, config, restore=False):
        self.config = config
        self.processor = widget.Munin2Widget(
            self.config,
            restore=restore
        )

    def run(self):
        app = aiohttp.web.Application()

        app.router.add_route("*", "/{tail:.*}", self.handle_request)

        quicklogging.info("all set up")

        aiohttp.web.run_app(
            app,
            port=self.config.port,
            host=self.config.listening_address,
        )

    async def handle_request(self, request):
        if request.method == "GET":
            quicklogging.debug("%s", request)
        if request.method == "POST":
            text = await request.text()
            self.processor.consume(text)

        return aiohttp.web.Response(text="Hello, world")
