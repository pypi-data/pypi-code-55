""" Cli interface for libvis modules and dev """
import click
import libvis_mods as wm

from libvis_mods.config_gen import with_libvis_config
from libvis_mods.publish import publish
from libvis_mods.utils import only_required_kwargs_call
from libvis_mods.download import repository

from libvis_mods.paths_config import (
    web_user_mods, python_user_mods
)


@click.group()
def cli(): pass

name = click.argument('modname', required=False)
back = click.argument('back_src'
                      , type=click.Path(exists=True), required=False)
front = click.argument('front_src'
                       , type=click.Path(exists=True), required=False)

files = lambda x: back( front(
    with_libvis_config(x)
))


## ## ## User ## ## ##

@cli.command()
@name
@files
def install(*args, **kwargs):
    """ Install a module from directory """
    print('Arguments', kwargs)
    only_required_kwargs_call(
        wm.install, *args, **kwargs)


@cli.command('list')
def list_():
    """ list installed modules """
    mods = wm.installed()
    print("\n".join(mods))

@cli.command()
@name
def uninstall(**kwargs):
    """ Uninstall module """
    wm.uninstall(kwargs['modname'])

## ## ## Utils ## ## ##

@cli.command()
@click.option('-o', '--output-dir', 'output_dir', default='.')
@click.argument('source')
def download(source, output_dir):
    """ Download source for the module into ./`module_name`"""
    repository.determine_repo_dir(source, output_dir)

@cli.command()
@click.option('--front', 'request', flag_value='front')
@click.option('--back', 'request', flag_value='back')
@click.option('--both', 'request', flag_value='both', default=True)
def where(request):
    """ Prints locations of where modules are installed """
    if request == 'back':
        print(python_user_mods.absolute())
    if request == 'front':
        print(web_user_mods.absolute())
    else:
        print('back: {}'.format(python_user_mods))
        print('front: {}'.format(web_user_mods))

## ## ## Developer ## ## ##

@cli.command()
@name
@files
def develop(*args, **kwargs):
    """ Run the web server in development mode with hot reload """
    print(args, kwargs)
    only_required_kwargs_call(
        wm.develop, *args, **kwargs)


@cli.command()
@click.option('-o', '--output-dir', 'output_dir', default='.')
@name
def init_file(modname, output_dir):
    wm.init_file(modname, output_dir=output_dir)

@cli.command()
@click.option('-o', '--output-dir', 'output_dir', default='.')
@name
def init_dir(modname, output_dir):
    wm.init_dir(modname, output_dir=output_dir)


cli.command()(publish)

if __name__ == '__main__':
    cli()
