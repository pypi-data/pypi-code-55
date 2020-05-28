import os
import fs
import fs.path
from fs.copy import copy_file
import importlib
from functools import partial
from collections import UserString
from urllib.parse import urlencode, urlparse
from pipemaker.utils.dotdict import dotdict
from .creds import gdrive

import logging

log = logging.getLogger(__name__)


class Fpath(UserString):
    """ a fstring that will be formatted into a Filepath. methods return Fpath objects
    Used to distinguish path strings from strings when passed to functions or printed
    """

    def __repr__(self):
        """ with class """
        return f"Fpath({self})"


class Filepath:
    """ single representation of file to wrap url, path, pyfs_url, pyfs_path

        * simpler api for most common usage. still can access underlying parts if needed.
        * one step methods e.g. exists, isdir
        * additional methods for interactive use in notebook e.g. load, save
    """

    # dict(fs=connection) cache as files on same filesystem can share one connection
    maxcache = 100
    cons = dict()

    def __init__(self, url, root=None):
        """
        splits fs, path, query:
        
        * fs is pyfilesystem fs. includes name; "://"; drive, bucket, username, password
        * path has leading "/" which must be removed where necessary e.g. pandas read/write. required for googledrivefs copy_file, move_file, root files
        * query starts with "?"

        :param url: standard format url except without "file://" e.g. s3://simonm3/mypath or googledrive:mypath
        :param root: root for fs. only needed if need to go outside the default tree. default local=current folder; default googledrive="" which is root.

        url format https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Generic_syntax
        .. note:: pyfs_url includes //. This works fine but parses top level path into fs.

        """
        url = url.replace("\\", "/")
        parsed = urlparse(url)

        # query creds
        self.query = ""
        if parsed.query:
            self.query = f"?{parsed.query}"
        # automatically add googledrive creds as with s3
        elif parsed.scheme == "googledrive":
            self.query = gdrive()

        # fs
        self.fs = ""
        if parsed.scheme:
            self.fs = f"{parsed.scheme}:"
        # for some cloud providers there will be no netloc e.g. googledrive root
        if parsed.netloc or self.query:
            self.fs = f"{self.fs}//{parsed.netloc}"

        # filesystem root. default is current folder
        if root:
            self.fs = f"{self.fs}{root}"

        # path. remove backrefs, duplicated separators
        self.path = fs.path.normpath(parsed.path)
        if not self.path.startswith("/"):
            self.path = f"/{self.path}"

    def __getstate__(self):
        """ required for pickle """
        return self.__dict__

    def __setstate__(self, d):
        """ required for pickle """
        self.__dict__ = d

    @property
    def ofs(self):
        """ return open filesystem here rather than __init__ as cannot be pickled """
        cons = self.cons

        # already in cache (share connection as many files use same filesystem)
        try:
            return cons[self.fs]
        except KeyError:
            pass

        # cache connections as 500ms overhead
        cons[self.fs] = fs.open_fs(f"{self.fs}{self.query}")
        if len(cons) > self.maxcache:
            cons.pop(cons.keys()[0])

        return cons[self.fs]

    @property
    def islocal(self):
        """ is local file system
        :return: True if local file system 
        """
        return isinstance(self.ofs, fs.osfs.OSFS)

    @property
    def url(self):
        """ filesystem and path. excludes query. excludes file://
        :return: standard format url (strips // if at the end of pyfs_url).
        Note the same file can have multiple urls with different filesystem roots
        """
        fs1 = self.fs.rstrip("/")
        return f"{fs1}{self.path}"

    def __repr__(self):
        """ class and url """
        return f"Filepath({self.url})"

    def __str__(self):
        """ basename without extension. useful for display as short name """
        filename = fs.path.basename(self.path)
        return fs.path.splitext(filename)[0]

    def __hash__(self):
        """ unique key for dict """
        return hash(self.url)

    def __eq__(self, other):
        """ equal if have same url """
        return self.url == other.url

    def __getattr__(self, method, *args, **kwargs):
        """ shortcut to ofs.method(path, *args, **kwargs) """
        if self.path == "/" and method == "exists":

            def check():
                """ check filesystem exists """
                try:
                    self.listdir()
                    return True
                except:
                    return False

            return check
        return partial(getattr(self.ofs, method), self.path, *args, **kwargs)

    def _get_driver(self, driver=None):
        """
        :param driver: name of driver to load/save. if None uses file extension or pkl
        :return: driver module
        """
        if driver is None:
            driver = fs.path.splitext(self.path)[-1] or ".pkl"
            driver = driver[1:]
        try:
            return importlib.import_module(f"pipemaker.filesystem.filedrivers.{driver}")
        except ModuleNotFoundError:
            log.error(
                f"No driver found for {driver}. You can _add_module one in the filedrivers folder."
            )
            raise

    def dirname(self):
        return fs.path.dirname(self.path)

    def load(self, driver=None):
        """ return file contents
        :param driver: function to load/save. if None uses file extension or pkl """
        driver = self._get_driver(driver)
        return driver.load(self)

    def save(self, obj, driver=None):
        """ save obj to file
        :param driver: function to load/save. if None uses file extension or pkl
        """
        path1, ext = fs.path.splitext(self.path)

        # save to temp file so file is not available until complete
        # remove pyfs // at end in case top level folder does not exist
        fs1 = self.fs.rstrip("/")
        temp = Filepath(f"{fs1}{path1}_TEMP123{ext}{self.query}")

        # todo workaround bug in googledrivefs. makedirs fails to create top level folder
        splitpath = temp.dirname().split("/")
        if len(splitpath) > 1:
            temp.ofs.makedir(splitpath[1], recreate=True)
        #######
        temp.ofs.makedirs(temp.dirname(), recreate=True)
        driver = self._get_driver(driver)
        driver.save(self, obj, temp)

        # release file
        temp.move(self.path)
