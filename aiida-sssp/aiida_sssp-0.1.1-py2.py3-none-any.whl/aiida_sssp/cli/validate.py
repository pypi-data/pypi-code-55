# -*- coding: utf-8 -*-
"""Commands to list instances of `SsspFamily`."""
import click

from aiida.cmdline.params import arguments, types
from aiida.cmdline.utils import decorators, echo

from .root import cmd_root


@cmd_root.command('validate')
@arguments.GROUP(type=types.GroupParamType(sub_classes=('aiida.groups:sssp.family.sssp',)))
@click.argument('filepath', type=click.File(), required=False)
@decorators.with_dbenv()
def cmd_validate(group, filepath):
    """Validate an `SsspFamily`."""
    import json
    from aiida.common.files import md5_from_filelike

    if filepath:
        metadata = json.load(filepath)
    else:
        metadata = group.get_parameters_node().attributes

    for upf in group.nodes:

        with upf.open(mode='rb') as handle:
            md5 = md5_from_filelike(handle)

        element = upf.element
        filename = upf.filename

        try:
            values = metadata[element]
        except KeyError:
            echo.echo_warning('metadata `{}` does not contain element `{}`'.format(filepath.name, element))
            continue

        inconsistencies = {}

        if filename != values['filename']:
            inconsistencies['name'] = (filename, values['filename'])

        if md5 != values['md5']:
            inconsistencies['md5'] = (md5, values['md5'])

        if inconsistencies:
            echo.echo_warning('inconsistencies for {}'.format(element), bold=True)
            for key, values in inconsistencies.items():
                echo.echo(' {:<6}: {} != {}'.format(key, values[0], values[1]))
