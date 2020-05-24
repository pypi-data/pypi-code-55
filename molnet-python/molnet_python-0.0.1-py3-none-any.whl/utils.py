import hashlib


class Config:
    def __init__(self, url, hash, smiles_col, tasks_lst, task_type, relative_path, files, split, metric):
        self.url = url
        self.hash = hash
        self.smiles_col = smiles_col
        self.tasks_lst = tasks_lst
        self.task_type = task_type
        self.relative_path = relative_path
        # extracted file list
        self.files = files
        # directly downloaded file name
        self.fname = url.rsplit('/', 1)[-1]
        self.split = split
        self.metric = metric

        self.load_fn = None

    def add_load_fn(self, fn):
        self.load_fn = fn

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    # this returns a string
    return hash_md5.hexdigest()

