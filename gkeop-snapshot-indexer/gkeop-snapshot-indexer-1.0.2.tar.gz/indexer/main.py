# -*- coding: utf-8 -*-

import click
import indexer
import os

@click.command()
@click.argument('src')
@click.argument('dest', default='./.snapshot_index')
def index(src, dest):
    if not os.path.exists(src):
        raise FileNotFoundError('Source directory not found: %s' % src)

    if os.path.exists(dest):
        raise FileExistsError('Dest directory already exists: %s' % dest)

    click.echo('Build an index of %s to %s' % (src, dest))
    s = indexer.Snapshot(src)
    indexer.Index(s, dest)

if __name__ == '__main__':
    index()
