import base64
import json
import sys
import typing as t
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Markup, contextfunction

from datapane.api import Asset, Markdown
from dp_common import ImportFileResp, import_local_file_from_disk, temp_fname


@contextfunction
def include_raw(ctx, name):
    """ Normal jinja2 {% include %} doesn't escape {{...}} which appear in React's source code """
    env = ctx.environment
    return Markup(env.loader.get_source(env, name)[0])


dirname = Path(__file__).parent
template_loader = FileSystemLoader([dirname, dirname / "../resources"])
template_env = Environment(loader=template_loader)
template_env.globals["include_raw"] = include_raw
template = template_env.get_template("template.html")


class ReportFileWriter:
    """ Collects/creates all data needed to display a local report, and generates the local HTML """

    # The data of the asset file itself stored as base64.
    # Calls to these data_urls mimic GCS and DRF calls on remote reports.
    data_urls: t.Dict[str, str] = {}

    # Asset file metadata used to display assets base on content-type, display tables based on dimensions etc..
    # On remote reports these objects also contain information on how to fetch the file itself.
    asset_metadata: t.Dict[str, t.Dict] = {}

    # Object containing dataset metadata. Comparable to a partial DatasetDetail on the FE,
    # or serialised models.Dataset in Django.
    dataset_objs: t.Dict = {}

    blocks: t.Union[Asset, Markdown]

    report_obj: t.Dict

    title: str
    visibility: str
    description: str

    def __init__(
        self,
        *blocks: t.Union[Asset, Markdown],
        title: str,
        visibility: str = "OWNER_ONLY",
        description: t.Optional[str] = None,
    ):
        self.title = title
        self.visibility = visibility
        self.description = description
        self.blocks = blocks
        self.encode_assets([b for b in blocks if isinstance(b, Asset)])
        self.create_report_obj()

    def write(self, path: str):
        r = template.render(
            assets=json.dumps(self.data_urls),
            asset_metadata=json.dumps(self.asset_metadata),
            report_obj=json.dumps(self.report_obj),
            dataset_objs=json.dumps(self.dataset_objs),
        )
        Path(path).write_text(r)

    def encode_assets(self, assets: t.List[Asset]):
        """ Convert asset files into base64 URLs that can be in-lined into the report HTML """
        for a in assets:
            ext: str = "".join(a.file.suffixes)
            if ext in [".df.json", ".csv", ".xlsx"]:
                encoded_body, file_resp = self.encode_arrow_asset(a)
                # e.g. a json asset may be uploaded as a table and have its
                # content-type change from json to arrow.
                a.content_type = file_resp.content_type
                self.create_asset_metadata(a, file_resp)
                self.create_ds_obj(a, file_resp)
            else:
                encoded_body = self.encode_asset(a)
                self.create_asset_metadata(a)
            self.data_urls[str(a.id)] = f"data:{a.content_type};base64,{encoded_body.decode()}"

    def create_asset_metadata(
        self, asset: Asset, file_resp: t.Optional[ImportFileResp] = None
    ) -> t.Dict:
        """ Mock (partial) serializer for Asset File object """
        self.asset_metadata[str(asset.id)] = {
            "id": asset.id,
            "title": asset.kwargs.get("title"),
            "content_type": asset.content_type,
            "size_bytes": file_resp.file_size if file_resp else sys.getsizeof(asset),
        }

    def create_ds_obj(self, asset: Asset, file_resp: t.Optional[ImportFileResp]) -> t.Dict:
        """ Mock (partial) serializer for Dataset model """
        self.dataset_objs[str(asset.id)] = {
            "num_rows": file_resp.num_rows,
            "num_columns": file_resp.num_columns,
            "cells": file_resp.num_rows * file_resp.num_columns,
            "size_bytes": file_resp.file_size,
            "schema": file_resp.schema,
            "id": asset.id,
            "title": asset.kwargs.get("title"),
            "username": "local-user",
        }

    def create_report_obj(self):
        """ Mock (partial) serializer for Django Report model """
        self.report_obj = {
            "blocks": [],
            "title": self.title,
            "visibility": self.visibility,
            "description": self.description,
            "id": "local00",
            "username": "local-user",
        }
        for idx, b in enumerate(self.blocks):
            block_obj = (
                self.markdown_block(b, idx) if isinstance(b, Markdown) else self.asset_block(b)
            )
            self.report_obj["blocks"].append(block_obj)

    def markdown_block(self, block: Markdown, idx: int) -> t.Dict:
        """ Mock serializer for Markdown block """
        return {"id": len(self.blocks) + idx, "content": block.content, "type": "MARKDOWN"}

    @staticmethod
    def asset_block(block: Asset) -> t.Dict:
        """ Mock serializer for Asset block """
        return {"id": int(block.id), "asset": "local", "type": "ASSET"}

    @staticmethod
    def encode_asset(asset: Asset) -> str:
        """ Convert a non-arrow Asset file into a base64 URL """
        with open(str(asset.file), "rb") as f:
            return base64.b64encode(f.read())

    @staticmethod
    def encode_arrow_asset(asset: Asset) -> t.Tuple[str, ImportFileResp]:
        """ For arrow assets, the binary arrow file needs to be imported before encoding """
        with temp_fname(".arrow", "wb") as arrow_fn:
            res = import_local_file_from_disk(asset.file, str(arrow_fn))
            encoded_body = base64.b64encode(Path(arrow_fn).read_bytes())
            return encoded_body, res
