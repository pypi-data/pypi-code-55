# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

from pathlib import Path
from typing import Dict

from kedro.context import KedroContext, load_context
from kedro.pipeline import Pipeline

from take_forecast.pipeline import create_pipelines


class ProjectContext(KedroContext):
	
	project_name = 'Forecast'
	project_version = '0.15.9'
	
	
	def _get_pipelines(self) -> Dict[str, Pipeline]:
		return create_pipelines()


def run_package():
	project_context = load_context(Path.cwd())
	project_context.run()


if __name__ == "__main__":
	run_package()
