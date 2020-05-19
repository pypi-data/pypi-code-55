from pathlib import Path
from .dataset import Dataset
from .repo import Repo
import tempfile
import tarfile
from typing import Optional, Iterable


class Engine:
    def __init__(self, home:str):
        home = Path(home)
        home.mkdir(parents=True, exist_ok=True)
        self.home = home

    def ls(self) -> Iterable[str]:
        for x in self.home.iterdir():
            if x.is_dir() or x.is_symlink():
                yield x.name

    def register(self, dirname:str, name:Optional[str]=None, force=False):
        dirname = Path(dirname).resolve()
        Dataset.validate(dirname)

        if name is None:
            name = dirname.name

        dataset_path = self.home / name
        if dataset_path.exists() or dataset_path.is_symlink():
            if not force:
                raise RuntimeError(f'Dataset {name} exists. Use "force" to purge and replace.')
            self.purge(name)
        assert not (dataset_path.exists() or dataset_path.is_symlink())
        dataset_path.symlink_to(dirname)

    def purge(self, name:str):
        dataset_path = self.home / name
        if dataset_path.is_symlink():
            dataset_path.unlink()
            return
        if not dataset_path.exists():
            return
        rmrf(dataset_path)  # rm -rf

    def push(self, name:str, repo:Repo, force=False):
        if not force and repo.exists(name + '.tgz'):
            raise RuntimeError(f'Dataset {name} already exist in repository {repo}. Use "force" to override.')
        with tempfile.TemporaryDirectory() as d:
            tgz_name = f'{d}/temp.tgz'
            make_tgz(self.home / name, tgz_name)
            repo.upload(tgz_name, name + '.tgz')

    def pull(self, name:str, repo:Repo, force=False):
        if self.is_local_dataset(name):
            if not force:
                raise RuntimeError(f'Local dataset {name} already ezist. Use "force" to override.')

        with tempfile.TemporaryDirectory() as d:
            tgz_name = f'{d}/temp.tgz'
            repo.download(name + '.tgz', tgz_name)

            if self.is_local_dataset(name):
                self.purge(name)

            unpack_tgz(tgz_name, self.home / name)

    def is_local_dataset(self, name:str) -> bool:
        return (self.home / name).exists()

    def dataset(self, name:str) -> Dataset:
        return Dataset(self.home / name)


def rmrf(path:Path):
    '''recursively removes directory "path"'''
    for x in path.iterdir():
        if x.is_dir():
            rmrf(x)
        else:
            x.unlink()
    path.rmdir()


def make_tgz(path, out):
    '''packs content of directory :path: into a TGZ file :out: '''
    path = path.resolve()
    with tarfile.open(out, 'w:gz') as tar:
        for x in path.iterdir():
            tar.add(x, x.name)


def unpack_tgz(name, out):
    with tarfile.open(name, 'r:gz') as tar:
        tar.extractall(out)
