import typer

from delairstack_cli import analytics, config, products


app = typer.Typer()
app.add_typer(analytics.app, name='analytics', help='Interact with Analytics')
app.add_typer(products.app, name='products', help='Interact with Products')


@app.command()
def configure():
    """ Configure your credentials to connect to the platform """
    config.setup()


if __name__ == "__main__":
    app()
