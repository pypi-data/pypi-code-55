import inspect
import types
import shutil
from .step import Step
from ..filesystem import Filepath, Fpath
from .. import utils
import os
from fs.move import move_dir

import logging

log = logging.getLogger(__name__)

HOME = os.path.expanduser("~")


class BasePipeline:
    """ pipeline of steps that convert inputs into outputs """

    def __init__(self):
        """
        fpath: user defined fstring that is formatted at runtime with name and pipeline.pipevars).
        Default is "{fs}/{root}/{path}/{name}{ext}"::

            fs: pyfilesystem e.g. osfs://, s3://, googledrive://, ftp://
            root: root data path. absolute or relative to cwd. Cannot be outside cwd.
            path: subpath to separate runs e.g. pilot, full; london, paris; january, february
            name: filled with name of function output often func.__name__
            ext: output file format e.g. .pkl, .xlsx

        rest of pipeline attributes are used to fill parameters at runtime. Example usage:

            * value used as a parameter for a function or any upstream function
            * Filepath to map a data item shared by multiple runs to a common location
            * Filepath to map a file to a remote location
        """
        # format string for file locations
        self.fpath = "{fs}/{root}/{path}/{name}{ext}"

        # recycle bin for deleted files
        self.recycle = f"{HOME}/_recycle"

        # these are the default used to fill fpath at runtime
        # the fpath can be set to any fstring. it will be filled at runtime by pipeline.pipevars + name
        self.pipevars = utils.dotdict()
        v = self.pipevars
        v.fs = ""
        v.root = "pipedata"
        v.path = ""
        v.ext = ".pkl"

        # map output to function that can produce it
        self._output2step = dict()

        # lock to new attributes. store in self.pipevars instead
        self._lock = True

    def __setattr__(self, key, value):
        """ new variables added to pipeline after __init__ are put in pipevars """
        # set var in object directly
        if (
            key in vars(self)
            or isinstance(vars(self.__class__).get(key), property)
            or key.startswith("_")
            or not self.__dict__.get("_lock")
        ):
            super().__setattr__(key, value)
            return

        # set var in self.pipevars
        if not hasattr(self.pipevars, key):
            # warning to highlight any spelling mistakes
            log.warning(f"added new variable {key} to pipevars")
        setattr(self.pipevars, key, value)

    def __getattr__(self, key):
        """ fallback to pipevars if attribute does not exist """
        if hasattr(self.pipevars, key):
            return self.pipevars[key]
        else:
            # enable hasattr to return False
            raise AttributeError

    @property
    def fpath(self):
        return self._fpath

    @fpath.setter
    def fpath(self, value):
        """ can be set as string or Fpath """
        if isinstance(value, str):
            value = Fpath(value)
        self._fpath = value

    def add(self, steps, strict=False):
        """ add steps to the pipeline

        :param steps: module, list of modules, function, list of functions
        :param strict: if true then functions are ignored unless they have return annotation or start get\\_, make\\_

        ..warning:: refers to calling frame so if moved then need to update the code to refer to correct frame
        """
        frame = inspect.currentframe()
        bglobals = frame.f_back.f_globals

        # convert single step to list
        if not isinstance(steps, list):
            steps = [steps]

        for step in steps:
            # already added
            if isinstance(step, Step):
                continue

            # invalid parameter
            if not inspect.ismodule(step) and not inspect.isfunction(step):
                raise Exception("add parameter should be either a module or a function")

            # add function
            if inspect.isfunction(step):
                if (
                    not step.__name__.startswith("_")
                    and step.__name__ in bglobals
                    and bglobals[step.__name__].__module__ == step.__module__
                ):
                    # add local ref e.g. func
                    bglobals[step.__name__] = self._add_func(step)
                else:
                    # add local module ref e.g. xxx.func
                    try:
                        fullname = step.__module__.split(".")
                        setattr(
                            bglobals[fullname[-1]], step.__name__, self._add_func(step),
                        )
                    except:
                        raise Exception(f"cannot find {step} in bglobals")
            else:
                # add all functions in module (import module)
                funcs = {
                    k: v
                    for k, v in vars(step).items()
                    if isinstance(v, types.FunctionType)
                    and not v.__name__.startswith("_")
                    and (v.__module__ == step.__name__)
                }
                for k, v in funcs.items():
                    # check excluded
                    if strict:
                        sig = inspect.signature(v)
                        if not (
                            sig.return_annotation != inspect.Parameter.empty
                            or v.__name__.startswith("make_")
                            or v.__name__.startswith("get_")
                        ):
                            continue
                    setattr(step, k, self._add_func(v))

                # add local module reference (from module import *)
                for k, v in bglobals.items():
                    if (
                        # user functions starting _ are assumed not part of a pipe
                        not k.startswith("_")
                        and isinstance(v, types.FunctionType)
                        # only add if part of this module
                        and v.__module__ == step.__name__
                    ):
                        bglobals[k] = self._add_func(v)
        del frame

    def name2filepath(self, name):
        """ convert name to filepath

        :param name: internal pipe name
        :return: pyfs filepath to physical location
        """
        path = getattr(self, name, self.fpath).format(name=name, **self.pipevars)
        return Filepath(path)

    def load(self, name):
        """ load data
        :param name: internal pipe name
        :return: contents of file
        """
        fp = self.name2filepath(name)
        try:
            return fp.load()
        except FileNotFoundError:
            log.error(f"File not found {self.url}")

    def save(self, obj, name):
        """ save data
        
        :param obj: data to save
        :param name: filename or pyfs url
        """
        fp = self.name2filepath(name)
        fp.save(obj)

    def _add_func(self, f, *args, **kwargs):
        """ decorator that wraps a function to create a Step """
        step = Step(self, f, *args, **kwargs)
        if not hasattr(step, "oname"):
            log.warning(f"{f.__name__} has no oname so not included in pipe")
            return f
        # store so steps can search for upstream steps to _add_func their inputs.
        self._output2step[step.oname] = step
        return step

    def reset_files(self, path=None):
        if path is None:
            src = Filepath(f"{self.fs}{self.root}")
        else:
            src = Filepath(f"{self.fs}{self.root}{path}")
        if src.isdir():
            dst = Filepath(f"{self.recycle}{src.path}", root="/")
            dst.makedirs(recreate=True)
            log.info(f"moving {src.path} to {dst.path}")
            move_dir(src.fs, src.path, dst.fs, dst.path)

    def reset(self, path=None):
        """ reset by moving files to self.recycle

        :param path: path to reset. None means root.
        """
        # reset files
        self.reset_files()

        # reset pipeline definition
        self._output2step.clear()

        # reset wrapped functions
        # typically relevant stack is 1 or 2 back so 5 should be plenty.
        currframe = inspect.currentframe()
        frame = currframe.f_back
        for x in range(4):
            bglobals = frame.f_globals
            for k, v in bglobals.items():
                if isinstance(v, Step):
                    bglobals[k] = v.func
            frame = frame.f_back
            if not frame:
                break
        del currframe

    def cleanup(self):
        """ cleanup temp folders """
        shutil.rmtree("_temp", ignore_errors=True)
        shutil.rmtree("_cache", ignore_errors=True)
