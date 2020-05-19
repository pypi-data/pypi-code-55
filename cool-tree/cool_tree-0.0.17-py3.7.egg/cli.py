import click
import rich
import rich.table
import rich.console

console = rich.console.Console()

@click.group()
def cli():
    pass


@cli.command()
@click.option('--profile_name', prompt='Profile Name', default='default')
@click.option('--access_key', prompt='Access Key')
def config(profile_name, access_key):
    while profile_name != 'default':
        click.prompt('Authentication failed. Please try again')
    click.echo(profile_name)
    click.echo(access_key)
    pass
    # helper_configure(show)


@cli.command()
def project():
    import spb
    table = rich.table.Table(show_header=True, header_style="bold magenta")
    table.add_column("NAME", width=12)
    table.add_column("LABELS")
    table.add_column("PROGRESS", justify="right")

    console.print(table)

@cli.command()
@click.argument('directory_name')
def init(dir_name):
    click.echo(dir_name)
    pass
    # helper_match(name)


@cli.command()
@click.argument('dataset_name')
@click.option('--log', 'log_file', type=click.File('a'))
@click.option('-f', '--force', 'is_force', is_flag=True)
def upload(dataset_name, log_file, is_force):
    click.echo(dataset_name)
    click.echo(log_file)
    click.echo(is_force)
    pass

@cli.command()
def download():
    pass