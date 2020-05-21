import atexit
import dataclasses as dc
import json
import os
import pickle
import pprint
import shutil
import time
import typing as t
import uuid
import webbrowser
from abc import ABC, abstractmethod
from collections import deque
from contextlib import contextmanager, suppress
from copy import copy
from pathlib import Path
from tempfile import NamedTemporaryFile, mkstemp
from urllib import parse as up

# TODO - import only during type checking and import future.annotations when dropping py 3.6
import pandas as pd
import pyarrow as pa
import requests
import validators as v
from munch import Munch, munchify
from requests import HTTPError, Response  # noqa: F401

from dp_common import (
    ARROW_MIMETYPE,
    JSON,
    PKL_MIMETYPE,
    URL,
    JDict,
    NPath,
    SDict,
    compress_file,
    log,
    setup_logging,
    temp_fname,
)
from dp_common.datafiles import convert_df_table, write_table
from dp_common.df_processor import process_df, to_df
from dp_common.scripts.config import DATAPANE_YAML, DatapaneCfg
from dp_common.utils import mimetype_for_file

from . import config as c
from ._version import __version__

###############################################################################
# top level functions here - move to runner?
# we're running on datapane platform
on_datapane: bool = "DATAPANE_ON_DATAPANE" in os.environ
# we're running the datapane runner (also checked by __name__ == "__datapane__" in user script)
by_datapane: bool = on_datapane or "DATAPANE_BY_DATAPANE" in os.environ

_report: t.Deque["Report"] = deque(maxlen=1)
# TODO - make thread/context safe and determine a better approach for vars
# TODO - add API tests


class _Params(dict):
    def load_defaults(self, config_fn: NPath = DATAPANE_YAML) -> None:
        if not by_datapane:
            log.debug(f"loading parameter defaults from {config_fn}")
            # TODO - move dp-server parameter handling into dp_common to use runnerconfig.format
            # NOTE - this is a bit hacky as we don't do any type formatting
            cfg = DatapaneCfg.create_initial(config_file=Path(config_fn))
            defaults = {p["name"]: p["default"] for p in cfg.parameters if "default" in p}
            self.update(defaults)
        else:
            log.debug("Ignoring call to load_defaults as by datapane")


Params: _Params = _Params()


@dc.dataclass
class _Result:
    result: t.Any = None

    def set(self, x: t.Any):
        self.result = x

    def get(self) -> t.Any:
        return self.result

    def exists(self) -> bool:
        return self.result is not None


Result = _Result()


def reset_api(params: SDict):
    """Called between each script invocation"""
    # TODO - refactor this all and make thread/context-safe
    Params.clear()
    Params.update(params)
    Result.set(None)


def init(
    config_env: str = "default",
    config: t.Optional[c.Config] = None,
    debug: bool = False,
    logs_stream: t.Optional[t.TextIO] = None,
):
    """Init the API - this MUST handle being called multiple times"""
    if c.get_config() is not None:
        log.debug("Already init")

    if config:
        c.set_config(config)
    else:
        config_f = c.load_from_envfile(config_env)
        log.debug(f"Loaded environment from {config_f}")

    setup_logging(verbose_mode=debug, logs_stream=logs_stream)


def is_jupyter():
    """Checks if inside ipython shell inside browser"""
    return (
        "get_ipython" in __builtins__
        and get_ipython().__class__.__name__ == "ZMQInteractiveShell"  # noqa: F821
    )


# TODO - make generic and return a dataclass from server?
#  - we can just use Munch and proxying for now, and type later if/when needed
#  - look at using types.DynamicClassAttribute
class Resource:
    # TODO - this should probably hold a requests session object
    endpoint: str
    headers: t.Dict
    url: str

    def __init__(self, endpoint: str, config: t.Optional[c.Config] = None):
        self.endpoint = endpoint.split("/api", maxsplit=1)[-1]
        self.config = config or c.config
        self.url = up.urljoin(self.config.server, f"api{self.endpoint}")
        self.headers = dict(Authorization=f"Token {self.config.token}")

    def _process_res(self, r: Response) -> JSON:
        if not r.ok:
            try:
                log.debug(pprint.pformat(r.json()))
            except ValueError:
                log.debug(pprint.pformat(r.text))
        r.raise_for_status()
        r_data = r.json()
        return munchify(r_data) if isinstance(r_data, dict) else r_data

    def post(self, params: t.Dict = None, **data: JSON) -> JSON:
        params = params or dict()
        # headers = {**self.headers, **{"Content-Type": "application/json"}}
        # json_data = json.dumps(data, default=lambda x: str(x))
        r = requests.post(self.url, json=data, params=params, headers=self.headers)
        return self._process_res(r)

    def get(self) -> JSON:
        r = requests.get(self.url, headers=self.headers)
        return self._process_res(r)

    def patch(self, **data: JSON) -> JSON:
        r = requests.patch(self.url, data, headers=self.headers)
        return self._process_res(r)

    def delete(self) -> None:
        r: Response = requests.delete(self.url, headers=self.headers)
        r.raise_for_status()

    @contextmanager
    def nest_endpoint(self, endpoint: str) -> t.ContextManager["Resource"]:
        """Returns a context manager allowing recursive nesting in endpoints"""
        a = copy(self)
        a.url = up.urljoin(a.url, endpoint)
        log.debug(f"Nesting endpoint {endpoint}")
        yield a
        log.debug(f"Unnesting endpoint {endpoint}")


# @dc.dataclass(frozen=True)
# class UserObjectDTO:
#     url: URL
#     id: str
#     isPublic: bool
#     parent: t.Optional[URL]
#     ...
#


class BEObjectRef:
    url: URL = "<local resource>"

    endpoint: str
    res: Resource
    # dto: UserObjectDTO
    dto: t.Optional[Munch] = None
    list_fields: t.List[str] = ["id", "title", "web_url"]

    @classmethod
    def _create_from_file(cls, file: Path, **kwargs) -> JSON:
        # get signed url
        upload_name = f"{int(time.time())}-{file.name}"
        upload_url = Resource("/generate-upload-url/").post(import_path=upload_name)
        # post text to blob store
        # TODO - we should disable compression where uneeded, e.g. .gz, .zip, .png, etc
        with compress_file(str(file)) as fn_gz, Path(fn_gz).expanduser().open("rb") as fp:
            log.info(f"Uploading {file}")
            headers = {"Content-Encoding": "gzip", "Content-Type": mimetype_for_file(file)}
            requests.put(upload_url, data=fp, headers=headers).raise_for_status()
        # post object to api
        return Resource(cls.endpoint).post(import_path=upload_name, **kwargs)

    def set_url(self, id_or_url: str):
        # build a url to the resource on the api server
        _id: str
        if self.endpoint in id_or_url:
            url = id_or_url
            if not url.startswith("http"):
                url = f"https://{url}"
            if not v.url(url):
                raise AssertionError(f"{url} is not a valid object ref")
            x: up.SplitResult = up.urlsplit(url)
            _id = list(filter(None, x.path.split("/")))[-1]
        else:
            _id = id_or_url

        rel_obj_url = up.urljoin(self.endpoint, f"{_id}/")
        self.res = Resource(endpoint=rel_obj_url)
        self.url = self.res.url

    # obj storage
    def get_obj(self) -> None:
        self.dto = self.res.get()

    @property
    def has_obj(self) -> bool:
        return self.dto is not None

    def __init__(self, id_or_url: str = None, dto: t.Optional[Munch] = None):
        if id_or_url:
            self.set_url(id_or_url)
            self.get_obj()
        elif dto:
            self.set_url(dto.url)
            self.dto = dto

    def __getattr__(self, attr):
        if self.has_obj and not attr.startswith("__"):
            log.debug(f"Proxying '{attr}' lookup to DTO")
            return getattr(self.dto, attr)
        # Default behaviour
        return self.__getattribute__(attr)

    def __str__(self) -> str:
        return self.url

    def __repr__(self) -> str:
        return pprint.pformat(self.dto.toDict()) if self.has_obj else self.__str__()

    # helper functions
    def refresh(self):
        """Update the local representation of the object"""
        self.get_obj()
        log.debug(f"Refreshed {self.url}")

    def delete(self):
        self.res.delete()
        log.debug(f"Deleted object {self.url}")

    def update(self, **kwargs):
        self.res.patch(**kwargs)
        self.refresh()
        log.debug(f"Updated object {self.url}")

    @classmethod
    def list(cls) -> t.Iterable[SDict]:
        """Return a list of the resources """
        endpoint: t.Optional[str] = cls.endpoint

        while endpoint:
            r = Resource(endpoint=endpoint)
            items = r.get()
            # filter the items, ordering as needed
            for x in items.results:
                yield {k: x[k] for k in cls.list_fields if k in x}
            endpoint = items.next if items.next else None


def download_file(download_url: str, fn: t.Optional[NPath] = None) -> NPath:
    """Downloiad a file to cwd, using fn if provided, else content-disposition, else tmpfile"""
    with requests.get(download_url, stream=True) as r:
        x = r.headers.get("Content-Disposition")
        if not fn:
            if x and "filename" in x:
                # 'attachment; filename="datapane_test_test_dp_1588192318-1588192318-py3-none-any.whl"'
                y = x.split("filename=", maxsplit=1)[1].strip('"')
                fn = str(Path.cwd() / y)
            else:
                f, fn = mkstemp()
                os.close(f)
        with open(fn, "wb") as f:
            # shutil.copyfileobj(r.raw, f)
            for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                f.write(chunk)
    return fn


class ExportableObjectMixin:
    def download_df(self) -> pd.DataFrame:
        with temp_fname(".arrow") as fn:
            download_file(self.gcs_signed_url, fn)
            df: pd.DataFrame = pa.ipc.open_file(fn).read_pandas()
        return df

    def download_file(self, fn: NPath):
        fn = Path(fn)

        # If file is of arrow type, export it. Otherwise use the gcs url directly.
        if self.content_type == ARROW_MIMETYPE:
            with self.res.nest_endpoint(
                endpoint=f"export/?export_format={self.get_export_format(fn)}"
            ) as nest_res:
                download_url = nest_res.get()
        else:
            download_url = self.gcs_signed_url
        download_file(download_url, fn)

    def download_obj(self) -> t.Any:
        with temp_fname(".obj") as fn_str:
            download_file(self.gcs_signed_url, fn_str)
            fn = Path(fn_str)
            # In the case that the original object was a Python object or bytes-like object,
            # the downloaded obj will be a pickle which needs to be unpickled.
            # Otherwise it's a stringified JSON object (e.g. an Altair plot) that can be returned as JSON.
            if self.content_type == PKL_MIMETYPE:
                with fn.open("rb") as fp:
                    return pickle.load(fp)
            else:
                return json.loads(fn.read_text())

    # TODO - generate these stats for all uploaded datasets
    def gen_df_describe(self, df, fn: Path):
        from .files import show

        try:
            desc = df.describe(include="all")
            show(desc, filename=fn)
        except ValueError:
            log.debug("Couldn't generate dataframe stats for empty dataframe")

    @staticmethod
    @contextmanager
    def save_df(df: pd.DataFrame, keep: bool = False) -> t.ContextManager[Path]:
        df = to_df(df)
        process_df(df)
        with temp_fname(".arrow", keep=keep) as fn:
            table = convert_df_table(df)
            write_table(table, fn)
            log.debug(f"Saved df to {fn} ({os.path.getsize(fn)} bytes)")
            yield Path(fn)

    @classmethod
    @contextmanager
    def save_obj(cls, data: t.Any, is_json: bool, keep: bool = False) -> t.ContextManager[Path]:
        # import here as a very slow module due to nested imports
        from .files import show

        out_fn = show(data, default_to_json=is_json)
        log.debug(f"Saved object to {out_fn} ({os.path.getsize(out_fn)} bytes)")
        # files.show has its own write logic outside temp_fname, so we re-implement unlinking the
        # file on exiting context. TODO - re-implement show to be a context manager?
        try:
            yield out_fn
        finally:
            if not keep:
                os.unlink(out_fn)

    @staticmethod
    def get_export_format(fn: Path) -> str:
        # TODO: Use DatasetFormats Enum
        valid_formats = [".df.json", ".csv", ".xlsx"]
        ext = "".join(fn.suffixes)
        if ext not in valid_formats:
            raise ValueError(
                f"Extension {ext} not valid for exporting table. Must be one of {', '.join(valid_formats)}"
            )
        return ext


class Blob(BEObjectRef, ExportableObjectMixin):
    endpoint: str = "/blobs/"

    @classmethod
    def upload_df(cls, df: pd.DataFrame, **kwargs) -> "Blob":
        with cls.save_df(df) as fn:
            res = cls._create_from_file(fn, **kwargs)
            return cls(dto=res)

    @classmethod
    def upload_file(cls, fn: NPath, **kwargs) -> "Blob":
        res = cls._create_from_file(Path(fn), **kwargs)
        return cls(dto=res)

    @classmethod
    def upload_obj(cls, data: t.Any, is_json: bool = False, **kwargs: JSON) -> "Blob":
        with cls.save_obj(data, is_json) as out_fn:
            res = cls._create_from_file(out_fn, **kwargs)
            return cls(dto=res)


class Script(BEObjectRef):
    endpoint: str = "/scripts/"

    @classmethod
    def upload_pkg(cls, sdist: Path, dp_cfg: DatapaneCfg, **kwargs) -> "Script":
        # merge all the params for the API-call
        kwargs["api_version"] = __version__
        new_kwargs = {**dp_cfg.to_dict(), **kwargs}
        res = cls._create_from_file(sdist, **new_kwargs)
        return cls(dto=res)

    def download_pkg(self) -> Path:
        # fn = Path(self.entrypoint.split(".")[0]).with_suffix(".whl")
        fn = download_file(self.gcs_signed_url)
        return Path(fn)

    def call(self, **params):
        """Download, install, and call the script with the provided params"""
        # NOTE - use __call__??
        # TODO - move exec_script here?
        # TODO - call should handle param defaults
        from dp_runner.exec_script import run

        run(self, params)

    def run(self, parameters=None, cache=True) -> "Run":
        """(remote) run the given app (cloning if needed?)"""
        parameters = parameters or dict()
        res = Resource("/runs/").post(script=self.url, parameter_vals=parameters, cache=cache)
        return Run(dto=res)

    def local_run(self, parameters=None) -> "Run":
        """(local) run the given script"""
        # NOTE -is there a use-case for this?
        raise NotImplementedError()
        # parameters = parameters or dict()
        # res = Resource("/runs/").post(script=self.url, parameter_vals=parameters, cache=cache)
        # return Run(dto=res)

    # @classmethod
    # def upload_str(cls, script: str, **kwargs) -> "Script":
    #     """Upload a function from the file (or current script?)"""
    #     with temp_fname(".py", keep=True) as fn:
    #         file = Path(fn)
    #         file.write_text(script)
    #     res = cls._create_from_file(file, **kwargs)
    #     return cls(dto=res)
    #
    # @classmethod
    # def upload_file(cls, script: NPath, **kwargs) -> "Script":
    #     raise NotImplementedError("disabled for now")
    #     res = cls._create_from_file(Path(script), **kwargs)
    #     return cls(dto=res)
    # def download_str(self) -> str:
    #     return self.source_code
    #
    # def download_file(self, fn: NPath) -> "Script":
    #     """Download to fn given"""
    #     fn = Path(fn)
    #     if fn.suffix == ".py":
    #         fn.write_text(self.download_str())
    #     elif fn.suffix == ".ipynb":
    #         with self.res.nest_endpoint(endpoint="export/") as nest_res:
    #             download_url: str = nest_res.post()
    #         log.debug(f"Downloading {download_url} to {fn}")
    #         _ = ur.urlretrieve(download_url, fn)
    #     else:
    #         raise NotImplementedError(f"Can't export script to {fn}")
    #     return self


class Asset(BEObjectRef, ExportableObjectMixin):
    """We handle Asset's differently as effectively have to store the user request until
    it's been attached to a Datapane Asset block"""

    endpoint = "/assets/"

    file: Path = None
    # user_owns_file determines whether Asset.file should be deleted on _post_update.
    # If the user created the asset via upload_file, the supplied file belongs to the user
    # and shouldn't be deleted. Otherwise it's a temp file created during Asset creation that should be deleted.
    user_owns_file: bool = False
    kwargs: JDict = None

    @classmethod
    def upload_file(cls, file: NPath, **kwargs: JSON) -> "Asset":
        return cls(file=file, kwargs=kwargs, user_owns_file=True)

    @classmethod
    def upload_df(cls, df: pd.DataFrame, **kwargs: JSON) -> "Asset":
        with cls.save_df(df, keep=True) as fn:
            return cls(file=str(fn), kwargs=kwargs)

    @classmethod
    def upload_obj(cls, data: t.Any, is_json: bool = False, **kwargs: JSON) -> "Asset":
        with cls.save_obj(data, is_json, keep=True) as out_fn:
            return cls(file=out_fn, kwargs=kwargs)

    def _post_update(self, block_id: int):
        block_url = up.urljoin(c.config.server, f"api/blocks/{block_id}/")
        res = self._create_from_file(self.file, report_block=block_url, **self.kwargs)
        # reset the object internally
        self.set_url(res.url)
        self.get_obj()
        # delete if the file object isn't user-owned
        self.remove_tmp_file()

    def remove_tmp_file(self):
        if not self.user_owns_file:
            os.unlink(self.file)

    def __init__(
        self,
        id_or_url: str = None,
        file: NPath = None,
        user_owns_file: bool = False,
        kwargs: JDict = None,
    ):
        self.user_owns_file = user_owns_file
        if id_or_url is not None:
            super().__init__(id_or_url)
        else:
            # building buffered version
            self.file = Path(file)
            self.kwargs = kwargs

    def __str__(self) -> str:
        return super().__str__() if self.has_obj else str(self.file)

    def __repr__(self) -> str:
        return super().__repr__() if self.has_obj else str(self.file)


@dc.dataclass(frozen=True)
class Markdown:
    content: str


# NOTE - hacks re API compatability
class Plot(Asset):
    @classmethod
    def create(cls, data: t.Any, **kwargs: JSON) -> "Asset":
        return Asset.upload_obj(data=data, **kwargs)


class Table(Asset):
    @classmethod
    def create(cls, df: pd.DataFrame, **kwargs: JSON) -> "Asset":
        return Asset.upload_df(df=df, **kwargs)


class Run(BEObjectRef):
    endpoint: str = "/runs/"

    def is_complete(self) -> bool:
        """Return true if the run has finished"""
        return self.status in ["SUCCESS", "ERROR", "CANCELLED"]


# @dc.dataclass()
# class Block:
#     # a subset of block types - we'll combine with munch for other dynamic attribs
#     refId: str
#     type: str
#     id: t.Optional[int] = None
#     dataset: t.Optional[URL] = None
#     function: t.Optional[URL] = None
#     content: t.Optional[str] = None


# Internal type to represent the blocks as exposed to the lib consumer
BlockType = t.Union[Asset, Markdown]


def mk_block(b: BlockType) -> JSON:
    r = Munch()
    r.ref_id = str(uuid.uuid4())
    if isinstance(b, Markdown):
        r.type = "MARKDOWN"
        r.content = b.content
    elif isinstance(b, Asset):
        r.type = "ASSET"
        r.asset = None  # block.asset
    return r


class BaseReport(ABC):
    @classmethod
    @abstractmethod
    def create(cls, *blocks: BlockType, **kwargs) -> "BaseReport":
        ...

    @abstractmethod
    def preview(self, width: int = 600, height: int = 500):
        ...

    @abstractmethod
    def open(self, **kwargs):
        ...


class Report(BEObjectRef, BaseReport):
    """create, run, and delete ops only, retrieve and update unsupported"""

    endpoint: str = "/reports/"

    @classmethod
    def create(cls, *blocks: BlockType, **kwargs) -> "Report":
        """Create a simple app based on datasets, dfs, and plots"""
        new_blocks = [mk_block(b) for b in blocks]
        # post report to api
        res = Resource(cls.endpoint).post(blocks=new_blocks, **kwargs)
        # upload assets and attach to the report
        #  - this is a bit hacky as relies on the ordering staying the same
        #  - could update by using refId
        log.info("Uploading assets for Report")
        for (idx, b) in enumerate(res.blocks):
            if b.type == "ASSET":
                asset: Asset = blocks[idx]
                asset._post_update(b.id)
        # recreate from url so have latest assets
        r = cls(res.url)
        _report.append(r)
        return r

    def open(self):
        raise NotImplementedError("")

    def __getitem__(self, key: int) -> JSON:
        """Return the block for the report"""
        return self.dto.blocks[key]

    def preview(self, width: int = 600, height: int = 500):
        # Preview reports inside IPython notebooks in browser
        if is_jupyter():
            from IPython.display import IFrame

            embed_url = self.embed_url
            if self.visibility != "PUBLIC":
                embed_url = self.private_embed_url
            return IFrame(src=embed_url, width=width, height=height)


class LocalReport(BaseReport):
    """ This doesn't implement BEObjectRef as the Resource/DTO operations aren't necessary """

    path: str
    tmpfile_name: str

    @classmethod
    def create(
        cls, *blocks: BlockType, path: str, title: str = "Local Report", **kwargs
    ) -> "LocalReport":
        from .report_file_writer import ReportFileWriter

        # local_assets is used to clean up any temp files once assets are encoded
        local_assets: t.List[Asset] = []
        for idx, b in enumerate(blocks):
            if isinstance(b, Asset):
                local_assets.append(b)
                # Mimic the lifecycle of a remote asset by setting these properties which are normally set in DRF
                b.id = idx
                b.content_type = mimetype_for_file(b.file)
        writer = ReportFileWriter(*blocks, title=title, **kwargs)
        writer.write(path)
        # Assets have now been encoded so it's safe to delete temp asset files
        for a in local_assets:
            a.remove_tmp_file()
        return cls(path=path)

    def open(self):
        webbrowser.open(f"file://{os.path.abspath(self.path)}", new=2)

    def preview(self, width: int = 600, height: int = 500):
        """ Preview reports inside IPython notebooks in browser """
        if is_jupyter():
            from IPython.display import IFrame

            with suppress(OSError, AttributeError):
                # Remove the previous temp report if it's been generated
                os.remove(self.tmpfile_name)

            # We need to copy the report HTML to a local temp file,
            # as most browsers block iframes to absolute local paths.
            Path("dp-tmp").mkdir(exist_ok=True)
            with NamedTemporaryFile(
                delete=False, dir="./dp-tmp", mode="w", prefix="dptmp", suffix=".html"
            ) as tmpfile:
                shutil.copy(self.path, tmpfile.name)
                self.tmpfile_name = f"dp-tmp/{os.path.basename(tmpfile.name)}"
            return IFrame(src=self.tmpfile_name, width=width, height=height)

    def __init__(self, path: str):
        self.path = path


class Variable(BEObjectRef):
    endpoint: str = "/settings/uservariables/"
    list_fields = ["id"]

    @classmethod
    def add(cls, value: str, visibility: str = "OWNER_ONLY"):
        res = Resource(cls.endpoint).post(value=value, visibility=visibility)
        return cls(res.id)


@atexit.register
def cleanup_tmp():
    # TODO - make `dp-tmp` a global constant
    shutil.rmtree("dp-tmp", ignore_errors=True)
