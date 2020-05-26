#!/usr/bin/env python3
"""
This file should be called after including this package as a git submodule
"""
import subprocess
import logging
import rna.path


class DialectModule(object):
    dialect = None

    def __init__(self, base_dir, module_name, repository_url=None):
        self._module_name = module_name
        self.base_dir = rna.path.Path(base_dir).resolve() / module_name
        self.dialect_dir = rna.path.Path(__file__).resolve().parent / self.dialect
        self.repository_url = repository_url
        self.place_holders = {'module_name': lambda: self.module_name}

    @classmethod
    def from_path(cls, path):
        path = rna.path.Path(path).resolve()
        module_name = path.name
        base_dir = path.parent
        return cls(base_dir, module_name)

    @property
    def module_name(self):
        """
        str: Name of the module
        """
        return self._module_name

    def src(self, rel_path):
        """
        Args:
            rel_path (pathlib.Path | str): file/folder path relative to the
                base directory

        Returns:
            pathlib.Path: Source directory
        """
        return self.dialect_dir / rel_path

    def dst_rel_path(self, rel_path):
        """
        Args:
            rel_path (pathlib.Path | str): file/folder path relative to the
                base directory

        Returns:
            pathlib.Path: file/folder path relavtive to destination directory.
                Placeholders are replaced
        """
        # replace place_holders only in destination
        parts = rel_path.parts
        for ph in self.place_holders:
            if ph in parts:
                parts = list(parts)
                ind = parts.index(ph)
                parts[ind] = self.place_holders[ph]()
        rel_path = rna.path.Path(*parts)
        return rel_path

    def dst(self, rel_path):
        """
        Args:
            rel_path (pathlib.Path | str): file/folder path relative to the
                base directory

        Returns:
            pathlib.Path: Destination directory. Placeholders are replaced
        """
        rel_path = self.dst_rel_path(rel_path)
        return self.base_dir / rel_path

    def update(self, rel_path):
        """
        Run a git diff on a file and apply it

        Args:
            rel_path (str): see :func:`~rna.DialectModule.transfer`
        """
        with open(str(self.src(rel_path)), 'r') as f_open:
            if 'rna: +UPDATE' not in f_open.readline():
                return  # do not perform the update.
        # perform the update
        with rna.path.cd_tmp(self.base_dir):
            subprocess.check_call(['git', 'diff', self.src(rel_path), self.dst(rel_path),
                                   '|', 'git', 'apply'])

    def transfer(self, rel_path, method=rna.path.cp):
        """
        Transfer basic dialect files to the destination.
        If the file is found check wheter the first line of the file
        is containing
            'rna: +UPDATE'
        If so, apply a git diff between the files to the old file.

        Args:
            rel_path (str): relative path within dialect_dir
            method (callable with src, dst): e.g. rna.path.cp or os.symlink
        """
        src = self.src(rel_path)
        dst = self.dst(rel_path)
        if dst.exists():
            logging.info("Destination {dst} already existing"
                         .format(**locals()))

        else:
            method(src, dst)
            logging.info("Executing {method.__name__}({src}, {dst})".format(**locals()))

            # add the new file to git
            with rna.path.cd_tmp(self.base_dir):
                dst_rel_path = str(self.dst_rel_path(rel_path))
                subprocess.check_call(['git', 'add', dst_rel_path])
                logging.info("Adding newly added file {dst_rel_path} to main module git repo."
                             .format(**locals()))

    def start_project(self):
        """
        Built / update the project by transfering / updating files to it
        """
        # make the directory
        self.base_dir.mkdir(exist_ok=True)

        # init git
        # if not self.repository_url is None:
        #     raise NotImplementedError()
        # else:
        with rna.path.cd_tmp(self.base_dir):
            subprocess.check_call(['git', 'init'])

        # copy the dialect specific content to base_dir/<module_name>
        # rna.path.cp(self.dialect_dir, self.base_dir, exist_ok=True)
        for child in self.dialect_dir.glob('**/*'):
            # make the path relative
            rel_path = child.relative_to(self.dialect_dir)

            dst = self.dst(rel_path)
            if not dst.is_dir() and dst.exists():
                self.update(rel_path)
            else:
                # transfer the path
                self.transfer(rel_path)


class PythonModule(DialectModule):
    dialect = 'python'


if __name__ == '__main__':
    main()
