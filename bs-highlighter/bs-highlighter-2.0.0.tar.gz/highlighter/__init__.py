__all__ = ['highlight', 'lexers', 'styles']

from .highlight import highlight

def cli():
	from .cli import cli
	cli()

def server_cli():
	from . import server as m
	m.cli()