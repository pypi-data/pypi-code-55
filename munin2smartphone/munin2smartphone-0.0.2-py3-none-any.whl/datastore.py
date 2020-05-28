import datetime
import json
import os
import pytz

import quicklogging
import yaml

from . import utils


class CheckItem(yaml.YAMLObject):
    yaml_tag = "!CheckItem"

    def __init__(self, data):
        self.label = data["label"]
        self.value = data["value"]
        self.extra = data["extra"] or None

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(loader.construct_mapping(node))

    @classmethod
    def to_yaml(cls, dumper, liveobject):
        return dumper.represent_mapping(
            cls.yaml_tag,
            {
                "label": liveobject.label,
                "value": liveobject.value,
                "extra": liveobject.extra,
            }
        )


class Check(yaml.YAMLObject):
    yaml_tag = "!Check"

    def __init__(self, data, time):
        # {'group': '2p', 'host': 'magellan.2p', 'graph_category': 'disk',
        # 'graph_title': 'Disk usage in percent', 'warning': [{'label':
        # '/mnt/backups', 'value': '93.04', 'w': ':92', 'c': ':98', 'extra':
        # ''}]}

        self.time = time
        self.host = data["host"]
        self.group = data["group"]

        # first get works with json, second with yaml
        self.category = data.get("graph_category") or data["category"]
        self.title = data.get("graph_title") or data["title"]

        if "level" in data:
            # from yaml cache
            self.level = data["level"]
        # other possibilities: from http json push
        elif "error" in data:
            self.level = "error"
        elif "warning" in data:
            self.level = "warning"
        elif "unknown" in data:
            self.level = "unknown"
        else:
            self.level = "ok"

        # data["subchecks"] exists when loading yaml cache
        self.subchecks = data.get("subchecks") or []

        # fill from munin structure
        for level in ("error", "warning", "unknown", "ok"):
            for item in data.get(level, ()):
                self.subchecks.append(CheckItem(item))

        self.key = f"{self.group} {self.host} {self.category} {self.title}"

    @property
    def icon(self):
        if self.category == "disk":
            return "harddisk.png"
        return "point.png"

    def diff(self, other):
        if other is None:
            return f"nothing → {self.time} - {self.level}"
        if self.level == other.level:
            return None
        return f"{other.time} - {other.level} → { self.time } - {self.level}"

    @classmethod
    def to_yaml(cls, dumper, liveobject):
        return dumper.represent_mapping(
            cls.yaml_tag,
            {
                "category": liveobject.category,
                "group": liveobject.group,
                "host": liveobject.host,
                "level": liveobject.level,
                "time": liveobject.time,
                "title": liveobject.title,
                "subchecks": liveobject.subchecks,
            }
        )

    @classmethod
    def from_yaml(cls, loader, node):
        mapping = loader.construct_mapping(node)
        return Check(mapping, mapping["time"])


class CheckStore(yaml.YAMLObject):
    yaml_tag = "!CheckStore"

    def __init__(self, restored_backend=None):
        self._backend = {}
        self._decoder = json.JSONDecoder()

        if restored_backend:
            for check in restored_backend:
                self._insert_check(check)

    def consume(self, jsontext):
        """Register checks from a concatenated json stream"""
        now_utc = datetime.datetime.now(pytz.timezone("UTC"))
        text = jsontext.lstrip()
        while text:
            jsonobj, index = self._decoder.raw_decode(text)

            self._consume_one(jsonobj, now_utc)

            # truncate consumed json (left part), then leading spaces.
            text = text[index:].lstrip()

    def _consume_one(self, data, now_utc):
        """Makes a check from a deserialized single json check representation

        :param dict data:
        :param datetime.datetime now_utc:
        """
        utils.purge_none(data)

        check = Check(data, now_utc)
        self._insert_check(check)

    def _insert_check(self, check):
        check_key = check.key

        previous_state = self._backend.get(check_key)
        diff = check.diff(previous_state)
        if diff:
            quicklogging.info("%s: %s", check_key, diff)

        self._backend[check_key] = check

    def getchecks(self):
        return self._backend.values()

    @classmethod
    def from_yaml(cls, loader, node):
        return CheckStore(loader.construct_sequence(node))

    @classmethod
    def to_yaml(cls, dumper, liveobject):
        return dumper.represent_sequence(
            cls.yaml_tag,
            liveobject._backend.values()
        )

    @classmethod
    def restore(cls, savefile):
        with open(savefile, "r") as savefd:
            cached_checks = yaml.load(savefd, yaml.FullLoader).values()
        return CheckStore(restored_backend=cached_checks)

    def save(self, savefile):
        """Dumps current data into a yaml file

        First: writes yaml to swp file
        Second moves this file in place

        As to avoid inconsistency in the yaml file if anything happens while
        saving.
        """
        savefile_swp = "{}.swp".format(savefile)
        with open(savefile_swp, 'w') as savefd:
            yaml.dump(self._backend, savefd)
        os.rename(savefile_swp, savefile)
