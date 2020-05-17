"""AMNES Entrypoint."""

from .cli import cli  # pragma: no cover


def main() -> None:  # pragma: no cover
    """Main Entrypoint."""
    cli(auto_envvar_prefix="AMNES")  # pylint: disable=unexpected-keyword-arg


if __name__ == "__main__":  # pragma: no cover
    main()
