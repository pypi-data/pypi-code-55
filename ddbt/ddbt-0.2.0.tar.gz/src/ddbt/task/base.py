import yaml
from abc import ABC, abstractmethod
from argparse import Namespace
from copy import deepcopy
from datetime import datetime
from difflib import unified_diff
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import attr
from dateutil.parser import parse
from dbt.adapters.base.impl import BaseAdapter
from dbt.adapters.factory import get_adapter, register_adapter
from dbt.clients.system import run_cmd
from dbt.compilation import compile_manifest
from dbt.config import PROFILES_DIR, RuntimeConfig
from dbt.contracts.graph.manifest import Manifest
from dbt.exceptions import RuntimeException
from dbt.graph.selector import NodeSelector
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.node_types import NodeType
from dbt.perf_utils import get_full_manifest
from dbt.task.generate import Catalog
from dbt.ui.printer import green, red, yellow
from jinja2 import Template

from ddbt.constants import (
    GIT_CURRENT_CHANGES,
    GIT_LAST_CHANGES,
    GRANULARITY_STEP,
    get_commit_diff,
)


@attr.s(auto_attribs=True)
class BaseTask(ABC):
    # Models
    models: List[str] = attr.ib(default=attr.Factory(list))
    exclude: List[str] = attr.ib(default=attr.Factory(list))
    # Materialization
    materialization: List[str] = attr.ib(default=attr.Factory(list))
    # Args
    args: Namespace = attr.ib(
        default=Namespace(profiles_dir=PROFILES_DIR, project=None, profile=None)
    )
    # No init
    config: RuntimeConfig = attr.ib(init=False)
    manifest: Manifest = attr.ib(init=False)
    adapter: BaseAdapter = attr.ib(init=False)
    processed: int = attr.ib(init=False, default=0)
    errors: int = attr.ib(init=False, default=0)

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_args(cls, args):
        raise NotImplementedError

    @staticmethod
    def file_to_model(filename: str) -> str:
        """Convert file uri to model name.

        Args:
            filename (str): filename uri.

        Returns:
            str: model name
        """
        return Path(filename).stem

    @staticmethod
    def _build_query(
        resource_types: List[NodeType],
        models: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
    ) -> Dict[str, Optional[List[str]]]:
        """Create query for selecting models.

        Args:
            resource_types (List[NodeType]): resource type
            models (Optional[List[str]], optional): list of models to include.
                Defaults to None.
            exclude (Optional[List[str]], optional): list of models to exclude.
                Defaults to None.

        Returns:
            Dict[str, Optional[List[str]]]: query dictionary
        """
        return {
            "include": models,
            "exclude": exclude,
            "resource_types": resource_types,
            "tags": [],
        }

    def _get_config(self):
        """Get dbt configuration."""
        try:
            self.config
        except AttributeError:
            self.config = RuntimeConfig.from_args(self.args)
            register_adapter(self.config)

    def _get_adapter(self):
        """Get adapter."""
        self._get_config()
        logger.debug("Getting adapter.")
        self.adapter = get_adapter(self.config)

    def _load_manifest(self):
        """Load DBT manifest."""
        try:
            self.manifest
        except AttributeError:
            self._get_config()
            logger.debug("Loading manifest.")
            self.manifest = get_full_manifest(self.config)

    def _get_config_vars(self) -> Dict[str, Any]:
        self._get_config()
        variables = self.config.models.get(self.config.project_name).get("vars")
        return variables

    def _select_nodes(
        self,
        resource_types: List[NodeType],
        models: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
    ) -> Set[str]:
        """Select models from manifest.

        Args:
            resource_types (List[NodeType]): resource type
            models (Optional[List[str]], optional): list of models to include.
                Defaults to None.
            exclude (Optional[List[str]], optional): list of models to include.
                Defaults to None.

        Returns:
            Set[str]: list of model names
        """
        linker = compile_manifest(self.config, self.manifest)
        selector = NodeSelector(linker.graph, self.manifest)
        selected_nodes = selector.select(
            self._build_query(resource_types, models, exclude)
        )
        return selected_nodes

    def _get_filtered_manifest(
        self,
        resource_types: List[NodeType] = NodeType.executable(),
        models: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
        materialization: Optional[List[str]] = None,
    ) -> Manifest:
        """Get filtered manifest.

        Args:
            resource_types (List[NodeType], optional): resource type.
                Defaults to NodeType.executable().
            models (Optional[List[str]], optional): list of models to include.
                Defaults to None.
            exclude (Optional[List[str]], optional): list of models to exclude.
                Defaults to None.
            materialization (Optional[List[str]], optional): Materialization
                type to filter. Defaults to None.

        Returns:
            Manifest: filtered manifest
        """
        selected_nodes = self._select_nodes(resource_types, models, exclude)
        filtered_manifest = deepcopy(self.manifest)
        for key, node in self.manifest.nodes.items():
            if key not in selected_nodes or (
                materialization and node.get_materialization() not in materialization
            ):
                filtered_manifest.nodes.pop(key)
        return filtered_manifest


@attr.s(auto_attribs=True)
class GitTask(BaseTask):
    # Git
    cached_changes: bool = attr.ib(default=False)
    last_changes: bool = attr.ib(default=False)
    commit_diff: bool = attr.ib(default=False)
    commit_id: str = attr.ib(default="HEAD^")

    @staticmethod
    def git_command(cmd: List[str], filter_suffix: List[str]):
        """Get current modified and untracked models from git.

        Args:
            cmd (List[str]): command to run
            filter_suffix (List[str]): filter changes by suffix.

        Raises:
            RuntimeException: no models are found.

        Returns:
            Set[str]: Set of modifed and untracked files.
        """
        logger.debug(f"Running git command: {' '.join(cmd)}")
        out, _ = run_cmd(".", cmd, env={"LC_ALL": "C"})
        changes = out.decode("utf-8").strip().split("\n")
        result = {
            BaseTask.file_to_model(change)
            for change in changes
            if Path(change).suffix in filter_suffix
        }
        if not result:
            raise RuntimeException(f"No model changes found. Cmd: {' '.join(cmd)}")
        return result

    def _prepare_models(self) -> Optional[List[str]]:
        """Get list of models from git.

        Returns:
            Optional[List[str]]: List of models
        """
        prepare_models: Set[str] = set()

        # get git changes
        if self.cached_changes:
            prepare_models.update(self.git_command(GIT_CURRENT_CHANGES, [".sql"]))
        if self.last_changes:
            prepare_models.update(self.git_command(GIT_LAST_CHANGES, [".sql"]))
        if self.commit_diff:
            cmd = get_commit_diff(self.commit_id)
            prepare_models.update(self.git_command(cmd, [".sql"]))

        # get models from user input
        if self.models:
            prepare_models.update(self.models)

        # we need list of strings, when this list is empty it is necessary
        # to change it to None, otherwise NodeSelector wont return anything
        models = list(prepare_models) or None

        return models


@attr.s(auto_attribs=True)
class TimeRangeTask(BaseTask):
    start: str = attr.ib(default=datetime.now().strftime("%Y-%m-%d"))
    end: str = attr.ib(default=datetime.now().strftime("%Y-%m-%d"))
    granularity: str = attr.ib(default="days")
    increment: int = attr.ib(default=1)

    @staticmethod
    def _timestamp_vars(timestamp: datetime, prefix: Optional[str]) -> Dict[str, str]:
        """Get dictionary of formatted useful time variables. Prefix in case you need multiple
        timestamp instances like start, next, end.

        Args:
            timestamp (datetime): datetime to be formated
            prefix (Optional[str]): prefix for dictionary

        Returns:
            Dict[str, str]: dictionary of useful formatted variables
        """
        prefix = f"{prefix}_" if prefix else ""
        return {
            f"{prefix}timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            f"{prefix}date": timestamp.strftime("%Y-%m-%d"),
            f"{prefix}time": timestamp.strftime("%H:%M:%S"),
            f"{prefix}year": timestamp.strftime("%Y"),
            f"{prefix}month": timestamp.strftime("%m"),
            f"{prefix}week": timestamp.strftime("%W"),
            f"{prefix}day": timestamp.strftime("%d"),
            f"{prefix}daynumber": timestamp.strftime("%j"),
            f"{prefix}hour": timestamp.strftime("%H"),
            f"{prefix}minute": timestamp.strftime("%M"),
            f"{prefix}second": timestamp.strftime("%S"),
        }

    def time_range(self) -> List[Dict[str, str]]:
        """Get list of intevals and date variables for running the command.

        Returns:
            List[Dict[str, str]]: List of intervals to be run
        """
        start_timestamp = parse(self.start)
        end_timestamp = parse(self.end)
        time_range = []

        while start_timestamp <= end_timestamp:
            next_timestamp = start_timestamp + GRANULARITY_STEP[self.granularity](
                self.increment
            )
            time_vars = {
                "time_id": start_timestamp.strftime("%Y%m%d_%H%M%S"),
                "date_valid": start_timestamp.strftime("%Y-%m-%d"),
                "granularity": self.granularity,
                "increment": str(self.increment),
                **self._timestamp_vars(start_timestamp, "start"),
                **self._timestamp_vars(next_timestamp, "next"),
                **self._timestamp_vars(end_timestamp, "end"),
            }
            time_range.append(time_vars)
            start_timestamp = next_timestamp

        return time_range


@attr.s(auto_attribs=True)
class BootstrapTask(BaseTask):
    missing_only: bool = attr.ib(default=False)

    @abstractmethod
    def _render_stored(self, file_path: Path):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _merge_relations(
        database_rel: Dict[Any, Any], stored_rel: Dict[Any, Any]
    ) -> Dict[Any, Any]:
        raise NotImplementedError

    @staticmethod
    def _render_relation(relation: Dict[str, Any], template: Template) -> str:
        """Render relation template.

        Args:
            relation (Dict[str, str]): dictionary for rendering template
            template (Template): template to render

        Returns:
            str: rendered template
        """
        return template.render(**relation)

    @staticmethod
    def _get_input(input_text: str) -> str:
        """Get confirmation input.

        Args:
            input_text (str): text to show user to add input

        Returns:
            str: input written by user
        """
        confirm = input(input_text)
        return confirm

    @staticmethod
    def _write_template(rendered: str, rel_path: Path):
        """Write rendered template to path. Parent path is created if not exists.

        Args:
            rendered (str): rendered template
            rel_path (Path): path where to write template
        """
        rel_path.parent.mkdir(parents=True, exist_ok=True)
        rel_path.write_text(rendered)

    @staticmethod
    def _prepare_columns(columns: Dict[Any, Any]) -> List[Dict[str, str]]:
        """Prepare columns for rendering.

        Args:
            columns (Dict[Any, Any]): columns

        Returns:
            List[Dict[str, str]]: columns prepared for rendering
        """
        result = []
        for _, column in columns.items():
            col_dict = {
                "name": column.name.lower(),
                "data_type": column.type.lower(),
                "description": column.comment,
            }
            result.append(col_dict)
        return result

    @staticmethod
    def _prepare_render(
        name: str,
        columns: List[Dict[str, Optional[str]]],
        database: Optional[str],
        schema: Optional[str],
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Prepare data for rendering

        Args:
            name (str): relation name
            columns (List[Dict[str, Optional[str]]]): columns
            database (Optional[str]): database name
            schema (Optional[str]): schema name
            description (Optional[str], optional): relation description.
                Defaults to None.

        Returns:
            Dict[str, Any]: [description]
        """
        return {
            "database": database,
            "schema": schema,
            "name": name,
            "description": description,
            "columns": columns,
        }

    @staticmethod
    def _print_diff(difference: List[str]):
        """Pretty print difference.

        Args:
            difference (List[str]): List of differences
        """
        logger.info("-" * 40)
        for line in difference:
            if line.startswith("--") or line.startswith("++"):
                continue
            if line.startswith("@@"):
                logger.info(yellow(line))
                continue
            if line.startswith("-"):
                logger.info(red(line))
                continue
            if line.startswith("+"):
                logger.info(green(line))
                continue
            logger.info(line)

    @staticmethod
    def _compare_relation(db_rendered: str, stored_rendered: str) -> List[str]:
        """Compare stored and actual db relation and return changes.

        Args:
            db_rendered (str): actual database relation, rendered as yml file
            stored_rendered (str): actual stored relation, rendered as yml file

        Returns:
            List[str]: List of changes between two files
        """
        difference = list(
            unified_diff(stored_rendered.splitlines(), db_rendered.splitlines())
        )
        return difference

    def _set_catalog(self, manifest: Manifest, connection_name: str):
        """Initialize catalog

        Args:
            manifest (Manifest): manifest
            connection_name (str): name of connection
        """
        self._get_adapter()
        with self.adapter.connection_named(connection_name):
            logger.info("\nGetting list of relations from DB...")
            catalog_table, errors = self.adapter.get_catalog(manifest)
            logger.info(green("Done"))
        logger.info("\nCreating catalog...")
        catalog_data = []
        for row in catalog_table:
            tmp = dict(zip(catalog_table.column_names, row))
            # Lowercase database, schema, table name and table type for faster access
            tmp["table_database"] = tmp["table_database"].lower()
            tmp["table_schema"] = tmp["table_schema"].lower()
            tmp["table_name"] = tmp["table_name"].lower()
            catalog_data.append(tmp)
        self.catalog = Catalog(catalog_data)
        logger.info(green("Done"))

    def _prompt(
        self,
        file_path: Path,
        db_rendered: str,
        stored_yml: Dict[Any, Any],
        input_text: str,
    ):
        """Show prompt if path already exists.

        Args:
            file_path (Path): path of existent stored template
            db_rendered (str): actual database relation, rendered as yml file
            stored_yml (Dict[Any, Any]): actual stored relation
            input_text (str): input to be shown
        """
        confirm = self._get_input(input_text)
        # Update
        if confirm.lower() in ["m", "merge"]:
            db_rendered_yml = yaml.load(db_rendered, Loader=yaml.SafeLoader)
            merged = self._merge_relations(db_rendered_yml, stored_yml)
            logger.info(green(f"Updating file {file_path}!"))
            self._write_template(yaml.dump(merged, sort_keys=False), file_path)
        # Replace
        elif confirm.lower() in ["r", "replace"]:
            logger.info(green(f"Replacing file {file_path}!"))
            self._write_template(db_rendered, file_path)
        # Cancel
        elif confirm.lower() in ["c", "cancel"]:
            logger.info(yellow("Skipping!"))
        # Repeat
        else:
            self._prompt(
                file_path, db_rendered, stored_yml, input_text
            )  # pragma: no covered
