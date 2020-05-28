import yaml
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

import attr
from agate.table import Table
from dbt.contracts.graph.parsed import ParsedModelNode
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.node_types import NodeType
from dbt.task.generate import Catalog, CatalogTable
from dbt.ui.printer import green
from jinja2 import Template

from ddbt.task.base import BootstrapTask, GitTask


SCHEMA_YML_TEMPLATE = Template(
    """version: 2
models:
- name: {{name}}
  columns:
    {% for col in columns -%}
    - name: {{col['name']}}
      data_type: {{col['data_type']}}
    {% endfor %}
  """
)

PROMPT_MESSAGE = """
DB: {db}.{schema}.{name}
File: {file_path}
----------------------------------------
There is a difference between the version in the schema file and in the database.
Do you want to merge[m] changes, replace[r] changes or cancel[c] the operation? """


@attr.s(auto_attribs=True)
class BootstrapSchemaTask(BootstrapTask, GitTask):
    catalog_table: Table = attr.ib(init=False)

    @classmethod
    def from_args(cls, args):
        return cls(models=args.models, exclude=args.exclude, args=args)

    def _get_relations(self) -> Dict[str, CatalogTable]:
        """Get relations.

        Returns:
            Dict[str, CatalogTable]: relations
        """
        models = self._prepare_models()
        filtered_manifest = self._get_filtered_manifest(
            resource_types=NodeType.executable(),
            models=models,
            exclude=self.exclude,
            materialization=self.materialization,
        )
        catalog_data = [
            dict(zip(self.catalog_table.column_names, row))
            for row in self.catalog_table
        ]
        catalog = Catalog(catalog_data)
        rels = catalog.make_unique_id_map(filtered_manifest)
        return rels

    def _get_schema_path(self, manifest_rel: ParsedModelNode) -> Path:
        """Get path of schema

        Args:
            manifest_rel (ParsedModelNode): parsed model node

        Returns:
            Path: path where schema will be written
        """
        rel_path = Path(manifest_rel.root_path) / manifest_rel.original_file_path
        schema_path = rel_path.parent / "schemas" / f"{manifest_rel.identifier}.yml"
        return schema_path

    @staticmethod
    def _merge_relations(
        database_rel: Dict[Any, Any], stored_rel: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        """Merge database and stored relations.

        Args:
            database_rel (Dict[Any, Any]): actual database relation
            stored_rel (Dict[Any, Any]): actual stored relation

        Returns:
            Dict[Any, Any]: merged relation
        """
        merged = deepcopy(stored_rel)

        # udpate columns
        stored_cols = {v["name"]: v for v in stored_rel["models"][0]["columns"]}
        merged_cols = []
        for col in database_rel["models"][0]["columns"]:
            if col["name"] in stored_cols:
                col.update(stored_cols.get(col["name"]))
            merged_cols.append(col)
        merged["models"][0]["columns"] = merged_cols

        return merged

    def _render_stored(self, file_path: Path):
        opened_file = file_path.read_text()
        stored_yml = yaml.load(opened_file, Loader=yaml.SafeLoader)

        model = stored_yml.get("models")[0]
        columns = model.get("columns") or []

        prepared = self._prepare_render(
            database=None,
            schema=None,
            name=model.get("name"),
            description=model.get("description"),
            columns=columns,
        )

        rendered = self._render_relation(prepared, SCHEMA_YML_TEMPLATE)
        return rendered, stored_yml

    def _handle_relations(self):
        rels = self._get_relations()

        processed = 0
        for identifier, rel in rels.items():
            # Get relation definition from manifest
            manifest_rel = self.manifest.nodes.get(rel.unique_id)
            # Get location for saving schema
            schema_path = self._get_schema_path(manifest_rel)
            prepared = self._prepare_render(
                database=manifest_rel.database,
                schema=manifest_rel.schema,
                name=manifest_rel.identifier,
                description=rel.metadata.comment,
                columns=self._prepare_columns(rel.columns),
            )

            rendered = self._render_relation(prepared, SCHEMA_YML_TEMPLATE)

            if schema_path.exists() and not self.missing_only:
                stored_rendered, stored_yml = self._render_stored(schema_path)
                diff = self._compare_relation(rendered, stored_rendered)
                # There is a difference
                if len(diff) > 0:
                    self._print_diff(diff)
                    prompt_msg = PROMPT_MESSAGE.format(
                        db=manifest_rel.database,
                        schema=manifest_rel.schema,
                        name=manifest_rel.identifier,
                        file_path=schema_path,
                    )
                    self._prompt(schema_path, rendered, stored_yml, prompt_msg)
                    processed += 1
            else:
                logger.info(green(f"Writing file {schema_path}!"))
                self._write_template(rendered, schema_path)
                processed += 1

        if processed == 0:
            logger.info(green("\nCool, all schema files match DB!"))
        return processed

    def run(self):
        self._load_manifest()
        self._get_adapter()
        with self.adapter.connection_named("ddbt_bootstrap_schema"):
            logger.info("Getting list of relations from DB...")
            self.catalog_table, errors = self.adapter.get_catalog(self.manifest)

        result = self._handle_relations()
        return result, True
