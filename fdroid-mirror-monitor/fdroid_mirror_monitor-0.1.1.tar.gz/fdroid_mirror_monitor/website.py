#!/usr/bin/env python3

# stdlibs:
from datetime import datetime, timezone
from importlib.metadata import metadata
from os import makedirs, path, getenv
import pkg_resources
# external:
from jinja2 import Environment, FileSystemLoader
from json2html import json2html


pkg_resources.require
def create_html(report, dir):
    """
    Create html on current report.

    :param report: dict
    :param dir: output directory of html
    :param repo_name: headline 1
    """
    # generate html from template with jinja
    print('create htmls')
    template_dir = path.join(path.dirname(__file__), path.pardir, 'templates')
    template_dir = path.abspath(template_dir)

    # variables:
    mirror_names = []
    sourceurl = getenv('CI_PROJECT_URL', metadata(__package__)['Home-Page'])
    last_check = datetime.fromtimestamp(
        report['last_check'], tz=timezone.utc).strftime("%F %H:%M %Z")

    makedirs(dir, exist_ok=True)
    env = Environment(loader=FileSystemLoader(template_dir))
    env.trim_blocks = True
    env.lstrip_blocks = True

    # render mirror details subpages
    # detaildir = dir + '/mirrors'
    template = env.get_template('details.html')
    for mirror in report['mirrors']:
        mirror_names.append(mirror['name'])
        table = json2html.convert(json=mirror)
        # makedirs(detaildir + mirror[name], exist_ok=True)
        with open(path.join(dir, mirror['name'] + '.html'), 'w') as f:
            f.write(template.render(mirror=mirror, table=table,
                                    ref_name=getenv('CI_COMMIT_REF_NAME')))

    # render index.html
    template = env.get_template('index.html')
    index = template.render(mirror_names=mirror_names, sourceurl=sourceurl, report=report, last_check=last_check)
    with open(path.join(dir, 'index.html'), 'w') as fp:
        fp.write(index)
