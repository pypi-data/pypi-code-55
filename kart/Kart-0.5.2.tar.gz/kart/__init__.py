# from kart import miners, mappers, renderers
from livereload import Server
import os
import shutil
import argparse

# from server import RequestHandler
# from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
# from tornado.web import StaticFileHandler
# from werkzeug import Response
# import sys


class Kart:
    def __init__(self, miners=[], mappers=[], renderers=[], config={}):
        self.miners = miners
        self.mappers = mappers
        self.renderers = renderers
        self.config = config

    def prepare(self):
        self.site = {}
        for miner in self.miners:
            self.site.update(miner.collect())
        self.site["config"] = self.config

    def create_map(self):
        self.map = {}
        for mapper in self.mappers:
            self.map.update(mapper.map(self.site))

    def move_static(self):
        os.makedirs(self.build_location, exist_ok=True)
        for x in os.listdir(self.build_location):
            if os.path.isdir(os.path.join(self.build_location, x)):
                shutil.rmtree(os.path.join(self.build_location, x))
            else:
                os.remove(os.path.join(self.build_location, x))
        if "static" in os.listdir():
            shutil.copytree("static", os.path.join(self.build_location, "static"))

        if "root" in os.listdir():
            for top_level_file in os.listdir("root"):
                shutil.copyfile(
                    os.path.join("root", top_level_file),
                    os.path.join(self.build_location, top_level_file),
                )

    def write(self):
        for renderer in self.renderers:
            renderer.url_function = self.url
            renderer.render(self.map, self.site, build_location=self.build_location)

    def url(self, *name):
        name = ".".join(name)
        if not name:
            return ""
        if name in self.map.keys():
            result = self.map[name]["url"]
        elif name + ".1" in self.map.keys():
            result = self.map[name + ".1"]["url"]
        elif "/" in name:
            result = name
        else:
            return ""
        return self.config["base_url"] + result

    # def serve_url(self, environ, start_response):
    #     url = environ["PATH_INFO"]
    #     self.create_map()
    #     rendered_page = ""
    #     current_map = [x for x in self.map.values() if url == x["url"]]
    #     if not current_map:
    #         return
    #     for renderer in self.renderers:
    #         renderer.url_function = self.url
    #         a = renderer.render_single(current_map[-1], self.site)
    #         if a:
    #             rendered_page = a
    #     if rendered_page:
    #         response = Response(rendered_page)
    #         return response(environ, start_response)
    #
    # def serve(self, port=9000):
    #     self.prepare()
    #     server = Server(self.serve_url)
    #     server.watcher.ignore_dirs("_site")
    #     server.watch(".", self.prepare)
    #     server.serve(root=self.build_location, port=port, host="0.0.0.0")

    def serve(self, port=9000):
        self.build()
        server = Server()
        server.watcher.ignore_dirs("_site")
        server.watch(".", self.build)
        server.serve(root=self.build_location, port=port, host="0.0.0.0")

    # def serve_url(self, url):
    #     self.create_map()
    #     rendered_page = ""
    #     current_map = [x for x in self.map.values() if url == x["url"]]
    #     if not current_map:
    #         return
    #     for renderer in self.renderers:
    #         renderer.url_function = self.url
    #         a = renderer.render_single(current_map[-1], self.site)
    #         if a:
    #             rendered_page = a
    #     return rendered_page
    #
    # def serve(self, port=9000):
    #     serve_url = self.serve_url
    #     build_location = self.build_location = "_site"
    #
    #     class RequestHandler(SimpleHTTPRequestHandler):
    #         def __init__(self, *args, **kwargs):
    #             super().__init__(*args, directory=build_location, **kwargs)
    #
    #         def do_GET(self):
    #             html = serve_url(self.path)
    #             if not html:
    #                 return SimpleHTTPRequestHandler.do_GET(self)
    #             else:
    #                 self.send_response(200)
    #                 self.send_header("Content-type", "text/html")
    #                 self.end_headers()
    #                 self.wfile.write(bytes(html, "utf-8"))
    #                 return
    #
    #     self.prepare()
    #     self.move_static()
    #     handler = RequestHandler
    #     with ThreadingHTTPServer(("", port), handler) as httpd:
    #         try:
    #             httpd.serve_forever()
    #         except KeyboardInterrupt:
    #             print("Stopping dev server")
    #             sys.exit(0)

    def build(self, build_location="_site"):
        self.build_location = build_location
        self.prepare()
        self.create_map()
        self.move_static()
        self.write()

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "command", help="command to execute", choices={"build", "serve"}
        )
        parser.add_argument(
            "-p", "--port", help="port to bind to", default=9000, type=int
        )
        parser.add_argument("--production", action="store_true")
        args = parser.parse_args()
        if not args.production:
            self.config["base_url"] = ""
        if args.command == "build":
            self.build()
        if args.command == "serve":
            self.build_location = "_site"
            self.serve(args.port)
