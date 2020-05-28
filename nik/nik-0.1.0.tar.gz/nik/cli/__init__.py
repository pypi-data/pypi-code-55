#!/usr/bin/env python
# -*- coding: utf-8 -*-

def nik():

    import argparse

    from nik.cli.init import init
    from nik.cli.status import status
    from nik.cli.open import open_
    from nik.cli.create import create
    from nik.cli.config import config
    from nik.cli.show import show
    from nik.cli.rename import rename

    def helpme(args):
        parser['main'].print_help()

    parser = {}
    parser['main'] = argparse.ArgumentParser(prog = 'nik', description = 'Power of Zettelkasten')
    parser['main'].set_defaults(func = helpme)
    # Choose Zettelkasten directory explicitly
    parser['main'].add_argument('-d', '--directory', nargs = '?', help = 'Zettelkasten directory')
    subparsers = parser['main'].add_subparsers()

    parser['init'] = subparsers.add_parser('init', help = 'Make a directory a Zettelkasten')
    parser['init'].set_defaults(func = init)

    parser['status'] = subparsers.add_parser('status', help = 'Show info about Zettelkasten')
    parser['status'].set_defaults(func = status)

    parser['show'] = subparsers.add_parser('show', help = 'Show info about a zettel in the Zettelkasten')
    parser['show'].set_defaults(func = show)

    parser['open'] = subparsers.add_parser('open', help = 'Open zettel with specified ID in the Zettelkasten')
    parser['open'].set_defaults(func = open_)
    parser['open'].add_argument('id', metavar = 'ID', type = str, help = 'Specify zettel ID to open')

    parser['create'] = subparsers.add_parser('create', help = 'Create a new zettel for the Zettelkasten')
    parser['create'].set_defaults(func = create)
    parser['create'].add_argument('id', metavar = 'ID', nargs = '?', type = str, help = 'Specify ID for zettel to create')
    parser['create'].add_argument('-t', '--title', nargs = '?', type = str, help = 'Specify a title for your new zettel')
    parser['create'].add_argument('-e', '--edit', action = 'store_true', default = False, help = 'Specify to edit new zettel immediately')
    parser['create'].add_argument('-f', '--format', choices = ('markdown', 'org-mode', 'ascii-doc'), default = 'markdown', nargs = '?', type = str, help = 'Specify markup format for new zettel')

    parser['config'] = subparsers.add_parser('config', help = 'Show config or make changes to it')
    parser['config'].set_defaults(func = config)

    parser['rename'] = subparsers.add_parser('rename', help = 'Rename zettel ID from A to B')
    parser['rename'].set_defaults(func = rename)
    parser['rename'].add_argument(dest = 'from', help = 'Rename this zettel ID...')
    parser['rename'].add_argument(dest = 'to', help = '...to that ID')

    # Parse arguments and delegate to respective function
    args = parser['main'].parse_args()
    args.func(args)
