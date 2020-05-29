"""
File utilities.
"""

import os
import re
import yaml
import codecs
import six

from datetime import datetime

from .util import (make_directory, to_unicode, to_dict, set_data,
                   errorlines, DitzError)


# Base Ditz YAML tag.
DITZ_TAG = "!ditz.rubyforge.org,2008-03-06"

# Substitutions applied to the YAML representation, mainly for ditz
# backward compatibility, so that there are not too many spurious diffs
# when mixing pyditz and ditz.
substitutions = [
    # One space after the Ditz tags, like Ruby does it.
    (r'(%s/\S+)' % DITZ_TAG, r'\1 '),

    # Double-quotes instead of single-quotes in list/dict entries.
    (r"([-:]) '([^']*)'$", r'\1 "\2"'),

    # Blank line before the issue IDs.
    (r'\nid:', r'\n\nid:'),

    # One space after mapping keys.
    (r'(\n[^ ]+:)\n', r'\1 \n'),
]


def read_file(path):
    "Read a file."

    with codecs.open(path, "rb", encoding='utf-8') as fp:
        return fp.read()


def write_file(path, text):
    "Write a file."

    with codecs.open(path, "wb", encoding='utf-8') as fp:
        fp.write(text)


def read_yaml_file(path):
    "Read YAML data from a file."

    with codecs.open(path, "rb", encoding='utf-8') as fp:
        return yaml.safe_load(fp)


def read_object_file(path):
    """
    Read a Ditz object from a YAML file and normalize it.
    """

    obj = read_yaml_file(path)
    obj.normalize()

    return obj


def write_yaml_file(path, item, encoding='utf-8'):
    """
    Write a Ditz object to a YAML file.
    """

    output = yaml.dump(item, Dumper=DitzDumper, default_style=None,
                       default_flow_style=False, allow_unicode=True,
                       explicit_start=True, width=1000)

    if six.PY2:
        output = output.decode(encoding)

    for pat, repl in substitutions:
        output = re.sub(pat, repl, output)

    with codecs.open(path, "wb", encoding=encoding) as fp:
        fp.write(output)


class DitzDumper(yaml.dumper.SafeDumper):
    @classmethod
    def initialize(cls):
        cls.add_representer(str, cls.stringish_representer)
        cls.add_representer(six.text_type, cls.stringish_representer)
        cls.add_representer(datetime, cls.timestamp_representer)
        cls.add_representer(type(None), cls.null_representer)

    def stringish_representer(dumper, data):
        style = None
        if '\n' in data or (data and data[0] in '!&*['):
            style = '"'
            if '\n' in data[:-1]:
                for line in data.splitlines():
                    if len(line) > dumper.best_width:
                        break
                else:
                    style = '|'

        return yaml.nodes.ScalarNode('tag:yaml.org,2002:str', data,
                                     style=style)

    def timestamp_representer(dumper, data):
        # Add Z for ruby compatibility.
        value = "%s Z" % str(data.isoformat(' '))
        return yaml.nodes.ScalarNode(u'tag:yaml.org,2002:timestamp', value)

    def null_representer(dumper, data):
        return yaml.nodes.ScalarNode(u'tag:yaml.org,2002:null', '')


DitzDumper.initialize()


class DitzObject(yaml.YAMLObject):
    """
    Base class of a Ditz object appearing in a YAML file.

    Attributes:
        ditz_tag (str): Base YAML tag prefix.
        yaml_tag (str): YAML tag written to file.
        filename (str): YAML filename to read/write.
        attributes (list): List of recognized attributes.
        defaults (list): Defaults for new attributes.
        log_events (list): List of events.
    """

    yaml_dumper = DitzDumper
    yaml_loader = yaml.SafeLoader

    ditz_tag = DITZ_TAG
    yaml_tag = None
    filename = None
    validator = None
    attributes = []
    defaults = {}

    def write(self, dirname="."):
        """
        Write object to its YAML file.

        Args:
            dirname (str, optional): Directory to write file into.
        """

        make_directory(dirname)
        path = os.path.join(dirname, self.filename)
        write_yaml_file(path, self)

    def event(self, username, text, comment=None, timestamp=None):
        """
        Add an event to the object's ``log_events`` list.

        Args:
            username (str): User name.
            text (str): Event description.
            comment (str, optional): User comment.
            timestamp (datetime, optional): Time of the event.
        """

        time = timestamp or datetime.now()
        text = to_unicode(text)
        comment = to_unicode(comment) or ""
        self.log_events.append([time, username, text, comment])

    def update(self):
        """
        Update the object to the latest version.

        This adds defaults for attributes added since the original set.
        It's intended to update cached objects after reading.
        """

        for attr, default in self.defaults.items():
            if not hasattr(self, attr):
                setattr(self, attr, default)

    def normalize(self):
        """
        Normalize object to a valid Ditz object.
        """

        v = self.validator
        if not v:
            return

        data = to_dict(self)
        if v.validate(data):
            data = v.normalized(data)
            set_data(self, data)
        else:
            lines = ["invalid format:"] + list(errorlines(v.errors))
            text = "\n   ".join(lines)

            if self.filename:
                text = self.filename + ": " + text

            raise DitzError(text)

    @classmethod
    def requires(cls, attr):
        "Return whether an attribute is required in its file."

        schema = cls.validator.schema[attr]
        return schema.get('required', False)

    @classmethod
    def to_yaml(cls, dumper, data):
        value = []

        # Keep attributes sorted.
        for attr in data.attributes:
            obj = getattr(data, attr)
            if obj is not None or cls.requires(attr):
                node_key = dumper.represent_data(attr)
                node_value = dumper.represent_data(obj)
                value.append((node_key, node_value))

        return yaml.nodes.MappingNode(cls.yaml_tag, value)
