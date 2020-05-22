"""Click CLI Module."""
import click


class ListOption(click.Option):
    """Custom option to convert space delimited string to a list."""

    def type_cast_value(self, ctx, value):
        """Split the string or use the default."""
        if value == []:
            return []
        try:
            return list(value.split(" "))
        except Exception:
            raise click.BadParameter(value)


# pylint: disable=too-many-arguments

COMMON_OPTIONS = [
    click.option('--enable-standard-rules/--disable-standard-rules',
                 default=True,
                 help='Enable/disable the standard rule set ' +  # noqa: W504
                 'that ships with mc-nag.'),
    click.option('--custom-platform-rules-dir', '-C', multiple=True,
                 type=click.Path(exists=True), default=None,
                 help='Path to a directory containing custom rules. ' +  # noqa: W504
                 'Allows multiple.'),
    click.option('--list-tags', '-lt', is_flag=True, help="List of all available tags."),
    click.option('--enable-tags-only', '-t', cls=ListOption, default=[],
                 help="A quoted list of tags. Scan only those Rules."),
]
MAIN_OPTIONS = COMMON_OPTIONS + [
    click.option('--rules', is_flag=True,
                 help='Display information about all available rules.'),
    click.option('--filepath', '-f', type=click.Path(exists=True),
                 required=False),
    click.option('--output', '-o', default='text',
                 type=click.Choice(['text', 'json', 'yaml', 'none'],
                                   case_sensitive=False)),
    click.option('--paramfile', '-p', type=click.Path(exists=True)),
    click.option('--rule-param', multiple=True, default=None,
                 help='Pass parameters through to rules.  Allows multiple.' +  # noqa: W504
                 ' Format: --rule-param param1=value1 ' +  # noqa: W504
                 '--rule-param param2=value2'),
    click.option('--verbose', '-v', count=True)
]


def add_click_options(options):
    """Decorate with Click options."""

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options
