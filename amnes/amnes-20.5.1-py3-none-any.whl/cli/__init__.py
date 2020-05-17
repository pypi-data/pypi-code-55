"""AMNES 'cli' package."""

import click

from .. import __copyright__, __version__
from .controller import group as controller
from .ctl import group as ctl
from .utils import amnes_license, amnes_thirdparty
from .worker import group as worker

# BEGIN CLICK FUNCTION FIX #


def click_printexit_option(  # type: ignore
    flag: str, name: str, content: str, *param_decls, **attrs
):  # pylint: disable=missing-function-docstring # noqa: D103
    def decorator(function):  # type: ignore
        def callback(ctx, param, value):  # type: ignore #pylint: disable=unused-argument
            if value and not ctx.resilient_parsing:
                click.echo(content, color=ctx.color)
                ctx.exit()

        attrs.setdefault("is_flag", True)
        attrs.setdefault("expose_value", False)
        attrs.setdefault("help", f"Show {name} and exit.")
        attrs.setdefault("is_eager", True)
        attrs["callback"] = callback
        return click.option(*(param_decls or (f"--{flag}",)), **attrs)(function)

    return decorator


#  END  CLICK FUNCTION FIX #


@click.command(  # type: ignore
    cls=click.CommandCollection,
    name="amnes",
    help="Adaptive Meta-Framework for Network Experiment Studies",
    sources=[ctl, controller, worker],
)
@click_printexit_option("license", "license", amnes_license())  # type: ignore
@click_printexit_option("copyright", "copyright notice", __copyright__)  # type: ignore
@click_printexit_option(
    "thirdparty", "third-party libraries", amnes_thirdparty()  # type: ignore
)
@click.version_option(__version__)
def cli() -> None:
    """CLI Entrypoint."""
