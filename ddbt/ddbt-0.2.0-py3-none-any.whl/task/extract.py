import json
import yaml
from inspect import getmembers, isfunction
from pathlib import Path
from subprocess import Popen
from typing import Any, Callable, Dict, List, Optional, Tuple

import attr
from dbt.exceptions import RuntimeException
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.node_types import NodeType
from dbt.ui.printer import green, red, yellow
from jinja2 import (
    Environment,
    FileSystemLoader,
    Template,
    TemplateNotFound,
    select_autoescape,
)

import ddbt.extra.jinja_functions as jinja_functions
from ddbt.task.base import TimeRangeTask


PATH_VAR = "embulk_template_path"


@attr.s(auto_attribs=True)
class ExtractTask(TimeRangeTask):
    embulk_template: Optional[str] = attr.ib(default=None)
    sources: List[str] = attr.ib(default=attr.Factory(list))
    dont_run: bool = attr.ib(default=False)
    keep_template: bool = attr.ib(default=False)
    template_help: bool = attr.ib(default=False)

    jinja_env: Environment = attr.ib(init=False)

    @classmethod
    def from_args(cls, args):
        return cls(
            embulk_template=args.embulk_template,
            sources=args.sources,
            dont_run=args.dont_run,
            keep_template=args.keep_template,
            template_help=args.template_help,
            start=args.start,
            end=args.end,
            granularity=args.granularity,
            increment=args.increment,
            models=args.models,
            exclude=args.exclude,
            args=args,
        )

    def _get_profiles_vars(self) -> Dict[str, Any]:
        """Get all variables from profiles.yml

        Returns:
            Dict[str, Any]: profiles dictionary
        """
        profiles_vars = {}
        profiles_file = Path(self.args.profiles_dir) / "profiles.yml"
        if profiles_file.exists():
            profiles_vars = yaml.safe_load(profiles_file.read_text())
        return profiles_vars

    def _list_functions(self, fcn: Callable) -> List[Tuple[str, Callable]]:
        """List functions from module.

        Args:
            fcn (Callable): function callable

        Returns:
            List[Tuple[str, Callable]]: list of function
        """
        functions_list = [f for f in getmembers(fcn) if isfunction(f[1])]
        return functions_list

    def _set_jinja_env(self):
        """Create Jinja environment. Template path is taken from dbt_project variables.

        Raises:
            RuntimeException: Template folder not found.
        """
        # Take template path from dbt_project variables
        variables = self._get_config_vars()
        template_path = Path(variables.get(PATH_VAR))
        if not template_path.exists():
            raise RuntimeException(
                red(
                    f"Embulk template path is not set in variables or does not exist. "
                    f"Please add variable `{PATH_VAR}: [template path]` "
                    f"to `dbt_project.yml`"
                )
            )
        loader = FileSystemLoader(str(template_path.absolute()))
        self.jinja_env = Environment(
            loader=loader,
            autoescape=select_autoescape(["html"]),
            extensions=["jinja2.ext.do"],
        )
        # Add extra jinja functions
        for function in self._list_functions(jinja_functions):
            self.jinja_env.globals[function[0]] = function[1]

    @staticmethod
    def _yml_filename(name: str) -> str:
        """Get yaml filename with extension.

        Args:
            name (str): filename without extension

        Returns:
            str: filename with extension
        """
        return f"{name}.yml"

    @staticmethod
    def _jinja_filename(name: str) -> str:
        """Get jinja filename with extension.

        Args:
            name (str): filename without extension

        Returns:
            str: filename with extension
        """
        return f"{name}.jinja"

    def _log_template_params(self, params: Dict[str, Any]):
        logger.info("\nHELP: List of extra functions available in Jinja template:\n")
        for fce in self._list_functions(jinja_functions):
            logger.info(yellow("-" * 15))
            logger.info(f"{fce[0]}:")
            logger.info(yellow(fce[1].__doc__))
        logger.info("\nHELP: List of extra parameters usable in Jinja template:\n")
        logger.info(yellow(yaml.dump(params, default_flow_style=False)))

    def _get_sources(self) -> Dict[str, Dict[str, Any]]:
        """Get and prepare sources for rendering.

        Raises:
            RuntimeException: No source found

        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of sources
        """
        results = {}
        if self.sources:
            logger.info("Loading parameters from source definitions...")
            self._load_manifest()
            results = {
                f"{node.identifier}_source": node.to_dict()
                for _, node in self.manifest.nodes.items()
                if node.resource_type == NodeType.Source
                and node.identifier in self.sources
            }
            if not results:
                raise RuntimeException(
                    red(
                        f"No sources match your filter [{self.sources}]. "
                        f"Please change filter or add source."
                    )
                )
        return results

    def _get_models(self) -> Dict[str, Dict[str, Any]]:
        """Get and prepare models for rendering.

        Raises:
            RuntimeException: No model found

        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of models
        """
        results = {}
        if any([self.models, self.exclude]):
            logger.info("Loading parameters from models definitions (schema files)...")
            self._load_manifest()
            filtered = self._get_filtered_manifest(
                resource_types=[NodeType.Model],
                models=self.models,
                exclude=self.exclude,
                materialization=None,
            )
            for _, node in filtered.nodes.items():
                if not node.patch_path:
                    raise RuntimeException(
                        red(
                            f"Model {node.identifier} doesn't have appropriate schema. "
                            f"So some variables (e.g. columns) in jinja template "
                            f"may be missing."
                        )
                    )
                results[f"{node.identifier}_model"] = node.to_dict()
            if not results:
                raise RuntimeException(
                    red(
                        f"No models match your filter [models: {self.models},"
                        f" exclude: {self.exclude}]. Please change filter or add models"
                    )
                )
        return results

    def _interpret(self, status_code: int) -> bool:
        """Interpret result from Embulk.

        Args:
            status_code (int): status code

        Raises:
            RuntimeException: Error during execution

        Returns:
            bool: execution successful
        """
        if status_code == 0:
            return True
        else:
            raise RuntimeException(red("Error occured during Embulk execution!"))

    def _run_command(self, cmd: List[str], cwd: str) -> bool:
        """Run command.

        Args:
            cmd (List[str]): cmd to be run
            cwd (str): cwd

        Returns:
            bool: command was successful
        """
        logger.info(f"Running command {cmd}")
        # embulk doesnt have shebang so it has to run in shell
        with Popen(cmd, cwd=cwd, shell=True, bufsize=1, universal_newlines=True) as p:
            p.communicate()
            return self._interpret(p.returncode)

    def _get_rendered_path(self, template_name: str) -> Path:
        """Get path where template should be rendered.

        Args:
            template_name (str): template name

        Returns:
            Path: path location
        """
        path_ = (
            Path(self.config.project_root)
            / self.config.target_path
            / "embulk"
            / self._yml_filename(template_name)
        )
        return path_

    def _create_file_and_run(self, template_name: str, rendered: str):
        """Create temporary rendered template file and run it in Embulk.

        Args:
            template_name (str): Template name
            rendered (str): rendered Jinja template
        """
        rendered_template = self._get_rendered_path(template_name)
        rendered_template.unlink(missing_ok=True)
        rendered_template.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(rendered_template, "w") as f:
                logger.info(f"Rendering template into '{str(rendered_template)}'")
                f.write(rendered)
            if not self.dont_run:
                self._run_command(
                    cmd=[f"embulk run {rendered_template}"],
                    cwd=self.config.project_root,
                )
        finally:
            if self.keep_template or self.dont_run:
                pass
            else:
                logger.info(f"Deleting template from '{str(rendered_template)}'")
                rendered_template.unlink(missing_ok=True)

    def _get_template(self, item_dict: Optional[Dict[str, Any]] = None) -> Template:
        """Get Jinja2 template.

        Args:
            item_dict (Optional[Dict[str, Any]], optional): Item dictionary. It is
                parsed model or source from Manifest converted to dict.
                Defaults to None.

        Raises:
            RuntimeException: Template not found.

        Returns:
            Template: Jinja2 template
        """
        meta = item_dict.get("meta") if item_dict else None
        template_name = self._get_template_name(meta)
        try:
            template = self.jinja_env.get_template(template_name)
        except TemplateNotFound:
            raise RuntimeException(
                red(
                    f"Embulk template you specified "
                    f"({template_name}) "
                    f"does not exist!"
                )
            )
        return template

    def _get_template_name(self, meta: Optional[Dict[str, Any]] = None) -> str:
        """Get template name from parameter, source or model meta section.

        Args:
            meta (Optional[Dict[str, Any]], optional): Source or model meta section.
                Defaults to None.

        Raises:
            RuntimeException: No template was specified

        Returns:
            str: template name
        """
        template_name = None
        if self.embulk_template:
            template_name = self.embulk_template
        if meta:
            embulk_template = meta.get("embulk_template")
            if embulk_template:
                template_name = embulk_template
        if not template_name:
            raise RuntimeException(
                red(
                    f"No Embulk template specified. Please add parameter "
                    f"--embulk-template [template name] or add "
                    f"embulk_template: [template name] key to meta section"
                    f"of your source or schema definition."
                )
            )
        return self._jinja_filename(template_name)

    def _prerender(self, data, params):
        """Prerender parse items from dbt sources or models.

        Args:
            data ([type]): [description]
            params ([type]): [description]
        """
        if isinstance(data, (dict, list)):
            for k, v in data.items() if isinstance(data, dict) else enumerate(data):
                if isinstance(v, str):
                    tmp = v.replace("[[", "{{").replace("]]", "}}")
                    data[k] = self.jinja_env.from_string(tmp).render(params)
                self._prerender(v, params)

    def prepare_run(self):
        """Prepare template for running and run it in Embulk.
        """
        to_process = {**self._get_sources(), **self._get_models()}
        if not to_process:
            # If no source or model is specified, run just embulk template
            to_process = {self.embulk_template: {}}
        time_range = self.time_range()
        arg_vars = json.loads(self.args.vars) if hasattr(self.args, "vars") else {}
        profiles_vars = self._get_profiles_vars()
        project_vars = self._get_config_vars()
        target = self.config.target_name if self.config else ""

        for time_vars in time_range:
            for item_name, item_dict in to_process.items():
                template = self._get_template(item_dict)
                template_params = {
                    "date": time_vars,
                    "cli_vars": arg_vars,
                    "profiles": profiles_vars,
                    "project_vars": project_vars,
                    "target": target,
                }
                self._prerender(item_dict.get("meta"), template_params)
                template_params["rel"] = item_dict
                if self.template_help:
                    self._log_template_params(template_params)
                rendered = template.render(template_params)
                file_name = f"{item_name}_{time_vars.get('time_id')}"
                self._create_file_and_run(file_name, rendered)
                self.processed += 1

    def run(self):
        self._set_jinja_env()
        self.prepare_run()
        logger.info(green("Done"))
        return self.processed, True
