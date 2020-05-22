"""This module glues all components together"""

import distutils.dir_util as dir_util
import logging
import os
import sys
from pathlib import Path

from melthon.data import get_yaml_data, load_yaml_file
from melthon.middleware import MWLoader
from melthon.middleware import MWStep
from melthon.template import process_templates


def clean(output_path: Path):
    """Deletes generated and temporary files"""
    if output_path.is_dir():
        for sub in os.listdir(output_path):
            sub_path = output_path / sub
            if sub_path.is_dir():
                dir_util.remove_tree(sub_path)
            else:
                os.remove(sub_path)
        logging.debug('Cleaned output folder "%s"', output_path)
    else:
        logging.info('Output folder "%s" not found. Nothing deleted.', output_path)


def build(templates_path: Path, static_path: Path, data_path: Path, middleware_path: Path, output_path: Path,
          render_exceptions: bool, pretty_urls: bool):
    # Check if mandatory templates_path exist
    if not templates_path.is_dir():
        logging.error('Configured templates folder "%s" doesn\'t exist', templates_path)
        exit(1)

    # Initial context
    context = {}
    if data_path.is_dir():
        logging.info('Loading YAML data files ...')
        context['data'] = get_yaml_data(data_path)
    else:
        logging.warning('Configured data folder "%s" doesn\'t exist. Skipping data load.', data_path)

    # Get repeat config
    repeat_config = "repeat.yml"
    repeat_path = Path(repeat_config)
    if repeat_path.is_file():
        logging.info('Config "repeat.yml" found, loading started')
        context['repeat'] = load_yaml_file(repeat_path)
        logging.info('Repeat config loaded. Count: %s', len(context['repeat']))
    else:
        context['repeat'] = {}
        logging.warning('Config "repeat.yml" not found. Program will exit if any ".repeat" templates found')

    # Load middlewares
    mws = None
    if middleware_path.is_dir():
        # Add current directory to path.
        # This is required to be able to load the middlewares
        sys.path.append(os.getcwd())

        # Load middlewares
        mws = MWLoader(middleware_path)
    else:
        logging.warning('Configured middleware folder "%s" doesn\'t exist. Skipping middleware execution.',
                        middleware_path)

    # Delete and recreate output folder
    logging.info('Cleaning temporary and output folders ...')
    clean(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    # Execute middlewares "before" step
    if mws is not None:
        context = mws.execute_chain(MWStep.BEFORE, context)
        logging.debug('Context after middlewares "before" step: %s', repr(context))

    # Render pages
    logging.info('Rendering pages ...')
    process_templates(templates_path, output_path, context, render_exceptions, pretty_urls)

    # Copy static assets to output
    if static_path.is_dir():
        logging.info('Copying static assets to output ...')
        static_dir = str(static_path.resolve())
        output_dir = str(output_path.resolve())
        dir_util.copy_tree(static_dir, output_dir, update=True)
    else:
        logging.warning('Configured static folder "%s" doesn\'t exist. Skipping copy to output.', static_path)

    # Execute middlewares "after" step
    if mws is not None:
        context = mws.execute_chain(MWStep.AFTER, context)
        logging.debug('Context after middlewares "after" step: %s', repr(context))
