import json
import sys
import jsonlines
import time
import os
import yaml

from typing import List, Any

from msbase.subprocess_ import try_call_std

def load_json(path: str):
    with open(path, "r") as f:
        s = f.read()
        try:
            return json.loads(s)
        except json.decoder.JSONDecodeError:
            return json.loads(s.encode().decode('utf-8-sig'))

def np_encoder():
    import numpy as np # pylint: disable=import-error
    class NpEncoder(json.JSONEncoder):
        def default(self, obj): # pylint: disable=method-hidden
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return super(NpEncoder, self).default(obj)
    return NpEncoder

def write_json(stuff, path: str, encoder_cls=None):
    with open(path, 'w') as f:
        f.write(json.dumps(stuff, sort_keys=True, cls=encoder_cls))

def write_pretty_json(stuff, path: str, encoder_cls=None):
    with open(path, 'w') as f:
        f.write(json.dumps(stuff, indent=4, sort_keys=True, cls=encoder_cls))

def append_pretty_json(stuff, path: str):
    with jsonlines.open(path, mode='a') as f:
        f.write(stuff) # pylint: disable=no-member

def datetime_str():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ")

def load_jsonl(path: str):
    with jsonlines.open(path) as reader:
        return [obj for obj in reader] # pylint: disable=not-an-iterable

def file_size(path: str):
    return os.stat(path).st_size

def file_size_mb(path: str):
    return file_size(path) / 1024.0  / 1024.0

def find_files(dirpath, file_ext=None, dir_ext=None):
    for root, dirs, files in os.walk(dirpath, followlinks=True):
        if file_ext:
            for f in files:
                if f.endswith(file_ext):
                     yield os.path.join(root, f)
        if dir_ext:
            for d in dirs:
                if d.endswith(dir_ext):
                     yield os.path.join(root, d)

def unzip(ijs):
    return [ i for i, j in ijs ], [ j for i, j in ijs ]

def sha256sum(apk_path):
    stdout, _, _ = try_call_std(["sha256sum", apk_path], print_cmd=False, output=False)
    return stdout.split()[0].strip()

def readlines(f: str):
    with open(f, "r") as fh:
        return [ l.strip() for l in fh.readlines() ]

def writelines(lines: List[str], f: str):
    with open(f, "w") as fh:
        fh.write("\n".join(lines))

def appendline(line: str, f: str):
    with open(f, "a") as fh:
        fh.write(line.strip() + "\n")

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def getenv(k, default=None):
    v = os.getenv(k)
    if v is None and default is not None:
        v = default
    assert v
    eprint("%s=%s" % (k, v))
    return v

def log_progress(l: List[Any], desc=None, print_item=False):
    total = len(l)
    for i, item in enumerate(l):
        info = ""
        if desc:
            info += " " + desc
        if print_item:
            info += " " + str(item)
        print(f"Progress: {i}/{total}" + info, flush=True)
        yield item

def load_yaml(path: str):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def write_yaml(stuff, path: str):
    with open(path, 'w') as f:
        yaml.safe_dump(stuff, f, default_flow_style=False, sort_keys=False)

def compare_lines(f1: str, f2: str):
    l1 = set(readlines(f1))
    l2 = set(readlines(f2))
    l12 = l1.intersection(l2)
    print("%s: %s" % (f1, len(l1)))
    print("%s: %s" % (f2, len(l2)))
    print("%s: %s" % ("intersection", len(l12)))
