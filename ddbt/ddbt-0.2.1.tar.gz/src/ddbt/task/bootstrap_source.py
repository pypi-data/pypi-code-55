import copy
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import attr
import dbt.utils
from dbt.contracts.graph.compiled import NonSourceNode
from dbt.contracts.graph.manifest import Manifest
from dbt.contracts.graph.parsed import ParsedSourceDefinition
from dbt.exceptions import RuntimeException
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.node_types import NodeType
from dbt.task.generate import Catalog, CatalogKey, CatalogTable
from dbt.ui.printer import green, red, yellow
from jinja2 import Template

from ddbt.task.base import BootstrapTask, GitTask


SOURCE_YML_TEMPLATE = Template(
    """version: 2
sources:
- name: {{schema}}
  database: {{database}}
  schema: {{schema}}
  tables:
  - name: {{name}}
    columns:
    {% for col in columns -%}
    - name: {{col['name']}}
    {%- if col['description'] %}
      description: {{col['description']}}
    {%- endif %}
    {%- if col['data_type'] %}
      data_type: {{col['data_type']}}
    {%- endif %}
    {% endfor -%}"""
)

PROMPT_MESSAGE = """
DB: {db}.{schema}.{name}
File: {file_path}
----------------------------------------
There is a difference between the version in the source file and in the database.
Do you want to MERGE[m] changes, REPLACE[r] changes or CANCEL[c] the operation? """


@attr.s(auto_attribs=True)
class BootstrapSourceTask(BootstrapTask, GitTask):
    raw_database: Optional[str] = attr.ib(default="raw")
    source_path: str = attr.ib(default="./models/sources")

    parsed_sources: List[ParsedSourceDefinition] = attr.ib(
        init=False, default=attr.Factory(list)
    )
    missing_sources: Set[Tuple[str, str]] = attr.ib(
        init=False, default=attr.Factory(set)
    )
    catalog: Catalog = attr.ib(init=False)

    @classmethod
    def from_args(cls, args):
        return cls(
            models=args.models,
            exclude=args.exclude,
            materialization=args.materialization,
            cached_changes=args.cached_changes,
            last_changes=args.last_changes,
            commit_diff=args.commit_diff,
            commit_id=args.commit_id,
            missing_only=args.missing_only,
            raw_database=args.raw_database,
            source_path=args.source_path,
            args=args,
        )

    def _load_manifest(self):
        """Load manifest. Manifest is loaded even source file does not exists."""

        def _process_sources_for_node(
            manifest: Manifest, current_project: str, node: NonSourceNode
        ):  # noqa
            pass

        # Mock failing
        dbt.parser.manifest._process_sources_for_node = _process_sources_for_node
        super()._load_manifest()

    def _add_fake_source(self, manifest: Manifest, source_name: str):
        """Add fake source to manifest. It is dirty
        but useful for getting data from different schemas and databases from catalog.

        Args:
            manifest (Manifest): manifest
            source_name (str): Name of fake source
        """
        key = f"source.{source_name}"
        if key not in manifest.nodes:
            manifest.nodes[key] = ParsedSourceDefinition(
                database=self.raw_database,
                schema=source_name,
                resource_type=NodeType.Source,
                identifier=source_name,
                name=source_name,
                source_name=source_name,
                source_description="",
                description="",
                loader="",
                unique_id=key,
                fqn=[source_name],
                package_name="",
                root_path="",
                path="",
                original_file_path="",
            )

    def _find_sources(self, manifest: Manifest):
        """Find and sort out all sources in manifest.

        Args:
            manifest (Manifest): manifest
        """
        manifest_copy = copy.deepcopy(manifest)
        for node in manifest_copy.nodes.values():
            # If node is source
            if node.resource_type == NodeType.Source:
                self.parsed_sources.append(node)
            # If node is model
            for source_name, table_name in node.sources:
                # Try to get source
                target_source = manifest.resolve_source(
                    source_name.lower(),
                    table_name.lower(),
                    self.config.project_name,
                    node.package_name,
                )
                # Source does not exists
                if not target_source:
                    self._add_fake_source(manifest, source_name.lower())
                    self.missing_sources.add((source_name.lower(), table_name.lower()))

    def _get_source_path(self, schema: str, identifier: str) -> Path:
        """Get source path.

        Args:
            schema (str): schema name
            identifier (str): source identifier

        Returns:
            Path: source path
        """
        path_ = Path(self.source_path) / schema / f"{identifier}.yml"
        return path_

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
        merged = copy.deepcopy(stored_rel)

        # udpate columns
        stored_cols = {
            v["name"]: v for v in stored_rel["sources"][0]["tables"][0]["columns"]
        }
        merged_cols = []
        for col in database_rel["sources"][0]["tables"][0]["columns"]:
            if col["name"] in stored_cols:
                col.update(stored_cols.get(col["name"]))
            merged_cols.append(col)
        merged["sources"][0]["tables"][0]["columns"] = merged_cols

        return merged

    def _render_stored(self, file_path: Path) -> Tuple[str, Dict[str, Any]]:
        """Take stored source file and render it again.
        It is useful for finding the changes.

        Args:
            file_path (Path): location of source file

        Returns:
            Tuple[str, Dict[str, Any]]: rendered template, source dictionary
        """
        opened_file = file_path.read_text()
        stored_yml = yaml.load(opened_file, Loader=yaml.SafeLoader)

        source = stored_yml.get("sources")[0]
        table = source.get("tables")[0]
        columns = table.get("columns") or []

        prepared = self._prepare_render(
            database=source.get("database"),
            schema=source.get("schema"),
            name=table.get("name"),
            description=table.get("description"),
            columns=columns,
        )

        rendered = self._render_relation(prepared, SOURCE_YML_TEMPLATE)
        return rendered, stored_yml

    def _table_not_found(self, database: str, schema: str, name: str):
        logger.error(red(f"  Not found in database"))
        self.errors += 1

    def _process_source(self, source: CatalogTable):
        """Proces one source.

        Args:
            source (CatalogTable): Source
        """
        source_path = self._get_source_path(
            source.metadata.schema, source.metadata.name
        )
        # Prepare dictionary for rendering
        prepared = self._prepare_render(
            database=source.metadata.database,
            schema=source.metadata.schema,
            name=source.metadata.name,
            description=source.metadata.comment,
            columns=self._prepare_columns(source.columns),
        )
        # render relation
        rendered = self._render_relation(prepared, SOURCE_YML_TEMPLATE)

        # Test if file already exists
        if source_path.exists():
            stored_rendered, stored_yml = self._render_stored(source_path)
            diff = self._compare_relation(rendered, stored_rendered)
            # There is a difference
            if len(diff) > 0:
                self._print_diff(diff)
                prompt_msg = PROMPT_MESSAGE.format(
                    db=source.metadata.database,
                    schema=source.metadata.schema,
                    name=source.metadata.name,
                    file_path=source_path,
                )
                self._prompt(source_path, rendered, stored_yml, prompt_msg)
                self.processed += 1
            # No difference
            else:
                logger.info(yellow("  No change"))
        # If file not exists
        else:
            logger.info(green(f"Writing file {source_path}!"))
            self._write_template(rendered, source_path)
            self.processed += 1

    def _process_missing_sources(self):
        """Process missing sources."""
        logger.info("\nProcessing missing sources...")
        for missing in self.missing_sources:
            key = CatalogKey(self.raw_database, missing[0].lower(), missing[1].lower())
            table = self.catalog.get(key)
            logger.info(
                f"∙ {self.raw_database}.{missing[0].lower()}.{missing[1].lower()}"
            )
            if not table:
                self._table_not_found(
                    self.raw_database, missing[0].lower(), missing[1].lower()
                )
                continue
            self._process_source(table)
        logger.info(green("Done"))

    def _update_parsed_sources(self):
        """Update existing sources."""
        logger.info("\nUpdating existing sources...")
        for parsed in self.parsed_sources:
            key = CatalogKey(
                parsed.database.lower(),
                parsed.schema.lower(),
                parsed.identifier.lower(),
            )
            table = self.catalog.get(key)
            logger.info(
                f"∙ {parsed.database.lower()}.{parsed.schema.lower()}"
                f".{parsed.identifier.lower()}"
            )
            if not table:
                self._table_not_found(
                    parsed.database.lower(),
                    parsed.schema.lower(),
                    parsed.identifier.lower(),
                )
                continue
            self._process_source(table)
        logger.info(green("Done"))

    def run(self) -> Tuple[int, bool]:
        """Run task.

        Raises:
            RuntimeException: Sources not found in database.

        Returns:
            Tuple[int, bool]: number of processed items, state.
        """
        self._load_manifest()
        models = self._prepare_models()
        filtered_manifest = self._get_filtered_manifest(
            resource_types=NodeType.executable(),
            models=models,
            exclude=self.exclude,
            materialization=self.materialization,
        )
        self._find_sources(filtered_manifest)
        self._set_catalog(filtered_manifest, "ddbt_bootstrap_source")
        self._process_missing_sources()
        if not self.missing_only:
            # Get tables from already parsed and created sources
            self._update_parsed_sources()
        if self.errors > 0:
            logger.info("\n")
            raise RuntimeException(
                red(
                    f"Some sources[{self.errors}] were not found in database. "
                    f"Please, create them manually!"
                )
            )
        return self.processed, True
