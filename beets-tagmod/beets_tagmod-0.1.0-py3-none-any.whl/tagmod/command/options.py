from optparse import Option, OptionParser
from typing import Any

from beets import ui
from beets.ui import UserError

TAG_SPLIT_CHAR = ","


def parse_media_query_option(
    option: Option, option_string: str, value: Any, parser: OptionParser
) -> None:
    if not value:
        ui.print_("No media query provided. Interact with whole database.")

    parser.values.media_query = value  # type: ignore


def parse_tag_names_option(
    option: Option, option_string: str, value: Any, parser: OptionParser
) -> None:
    if not value:
        raise UserError("Missing media tag names to modify!")

    parser.values.tag_names = value.split(TAG_SPLIT_CHAR)  # type: ignore


media_query_option = Option(
    "-q",
    "--query",
    default="",
    action="callback",
    callback=parse_media_query_option,
    help="query for media item list where to apply tag modifications to",
)

tag_names_option = Option(
    "-t",
    "--tags",
    action="callback",
    callback=parse_tag_names_option,
    help="comma separated list of media tag names to modify",
)

tagmod_command_parser = OptionParser(
    usage=(
        "beet tagmod [options] "
        "<pattern1> <replacement1> <pattern2> <replacement2>..."
    ),
    description=(
        "Modify the tags of media items with pattern replacements. "
        "All pattern and replacement pairs are applied to all tags of all media items "
        "that match the query. Per default the query will match the whole library. "
        "More complex queries must be surrounded by quotes."
    ),
    epilog=(
        "The user must confirm the final storage of the modified tags after a review"
    ),
)
tagmod_command_parser.add_option(media_query_option)
tagmod_command_parser.add_option(tag_names_option)
