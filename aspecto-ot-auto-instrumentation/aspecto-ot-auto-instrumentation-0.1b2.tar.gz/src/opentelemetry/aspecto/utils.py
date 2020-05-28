import os
import json
import subprocess
from datetime import datetime


def read_aspecto_json():
    root_dir = os.path.abspath(os.curdir)
    try:
        f = open(root_dir + "/aspecto.json")
        data = f.read()
        token = json.loads(data)["token"]
        return token
    except Exception:
        return None


def fetch_git_hash():
    root_dir = os.path.abspath(os.curdir)
    """Try Get from HEAD file:"""
    f = None
    try:
        f = open(root_dir + "/.git/HEAD")
        rev = f.read()
        if ":" not in rev:
            return rev
    except:
        pass
    finally:
        if f is not None:
            f.close()

    """Try Get from git CLI:"""
    try:
        gitHash = subprocess.check_output(["git", "rev-parse", "HEAD"])
        return gitHash.decode("ascii").strip()
    except:
        return "python-agent-" + datetime.now().isoformat()
