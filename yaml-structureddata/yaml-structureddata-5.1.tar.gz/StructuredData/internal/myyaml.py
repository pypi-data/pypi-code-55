"""yaml utilities.
"""

import sys
import hashlib

try:
    import yaml
except ModuleNotFoundError:
    sys.exit("Fatal error: module yaml was not found.\n"
             "python yaml is a prerequisite for this program.\n"
             "You can install the missing module with one of\n"
             "the following commands\n"
             "pip:\n"
             "  pip install PyYAML\n"
             "Fedora/Redhat Linux:\n"
             "  dnf install python3-pyyaml\n"
             "Debian/Ubintu Linux:\n"
             "  apt-get install python3-yaml libyaml\n"
            )

__version__="5.1" #VERSION#

_YAML_MAJOR_VERSION= int(yaml.__version__.split(".")[0])

# pylint: disable=invalid-name

md5nodes= True

class MySerializer(yaml.serializer.Serializer):
    """This class replaces Serializer from yaml/serializer.py

    It generates the anchors in a different way.
    """
    def __init__(self, *args, **kwargs):
        yaml.serializer.Serializer.__init__(self,*args,**kwargs)
        self._md5_used= set()
    def generate_anchor(self, node):
        if not md5nodes:
            self.last_anchor_id += 1
            return self.ANCHOR_TEMPLATE % self.last_anchor_id
        #print repr(node)
        fingerprint= hashlib.md5(repr(node)).hexdigest()
        key= fingerprint
        cnt= 0
        while True:
            if not key in self._md5_used:
                self._md5_used.add(key)
                break
            cnt+=1
            key= "%s-%d" % (fingerprint, cnt)
        return key

class MyDumper(yaml.emitter.Emitter, MySerializer,
               yaml.representer.Representer, yaml.resolver.Resolver):
    """does the same as yaml/dumper.py but uses MySerializer.

    Note: sort_keys parameter is neeed for Representer since version 5.1 of
    pyyaml.
    """
    # pylint: disable=too-many-ancestors, too-many-locals
    def __init__(self, stream,
                 default_style=None, default_flow_style=None,
                 canonical=None, indent=None, width=None,
                 allow_unicode=None, line_break=None,
                 encoding=None, explicit_start=None, explicit_end=None,
                 version=None, tags=None, sort_keys=True):
        """initialize"""
        # pylint: disable=too-many-arguments
        yaml.emitter.Emitter.__init__(self, stream, canonical=canonical,
                                      indent=indent, width=width,
                                      allow_unicode=allow_unicode,
                                      line_break=line_break)
        MySerializer.__init__(self, encoding=encoding,
                              explicit_start=explicit_start,
                              explicit_end=explicit_end,
                              version=version, tags=tags)
        if _YAML_MAJOR_VERSION >=5:
            yaml.representer.Representer.__init__(self, default_style=default_style,
                                                  default_flow_style=default_flow_style,
                                                  sort_keys= sort_keys)
        else:
            yaml.representer.Representer.__init__(self, default_style=default_style,
                                                  default_flow_style=default_flow_style)
        yaml.resolver.Resolver.__init__(self)

def read_file(filename):
    """read data from a yaml file.
    """
    stream= open(filename, 'r')
    try:
        # FullLoader needed since version 5.1 of pyyaml:
        if _YAML_MAJOR_VERSION >=5:
            dict_= yaml.load(stream, Loader= yaml.FullLoader)
        else:
            dict_= yaml.load(stream)
    except yaml.reader.ReaderError as e:
        raise ValueError("cannot read YAML file: %s" % str(e))
    stream.close()
    return dict_

def read_string(st):
    """read yaml data from a string.
    """
    # FullLoader needed since version 5.1 of pyyaml:
    # pylint: disable= no-else-return
    if _YAML_MAJOR_VERSION >=5:
        return yaml.load(st, Loader= yaml.FullLoader)
    else:
        return yaml.load(st)

def write_string(data):
    """convert data to a yaml string.
    """
    return yaml.dump(data,
                     Dumper= MyDumper,
                     indent=4, default_flow_style=False)

def write_file(filename, data):
    """write data as a yaml file.
    """
    stream= open(filename, "w")
    yaml.dump(data, stream=stream,
              Dumper= MyDumper,
              indent=4, default_flow_style=False)
    stream.close()
