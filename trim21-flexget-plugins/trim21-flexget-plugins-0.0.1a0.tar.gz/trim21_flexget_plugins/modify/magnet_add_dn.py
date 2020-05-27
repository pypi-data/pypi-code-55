import urllib.parse

from flexget import plugin
from flexget.event import event
from loguru import logger

logger = logger.bind(name="magnet_add_dn")


class PluginMagnetAddDownloadName:
    schema = {"type": "boolean"}

    @staticmethod
    def add_dn(magnet, title) -> str:
        u: urllib.parse.ParseResult = urllib.parse.urlparse(magnet)
        qs = urllib.parse.parse_qs(u.query, keep_blank_values=True)
        if "dn" not in qs:
            qs["dn"] = [title]
        query = urllib.parse.urlencode(qs, doseq=True, safe=":+")
        return urllib.parse.ParseResult(
            scheme=u.scheme,
            netloc=u.hostname,
            path=u.path,
            params=u.params,
            query=query,
            fragment=u.fragment,
        ).geturl()

    # Run after download plugin to only pick up entries it did not already handle
    @plugin.priority(0)
    def on_task_output(self, task, config):
        if not config:
            return
        for entry in task.accepted:
            entry["url"] = self.add_dn(entry["url"], entry["title"])
            if "urls" in entry:
                entry["urls"] = [self.add_dn(x, entry["title"]) for x in entry]


@event("plugin.register")
def register_plugin():
    plugin.register(PluginMagnetAddDownloadName, "magnet_add_dn", api_ver=2)
