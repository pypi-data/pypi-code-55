import optparse
from typing import Dict, List

from beets import library, ui
from beets.library import Item
from beets.ui import UserError, decargs

from beetsplug.tagmod.command.arguments import (
    parse_arguments_as_tag_modifications,
)
from beetsplug.tagmod.modification import modify_media_item_tag

CONFIRMATION_PROMPT = "\nDo you really want to save the modified tags? (y|n)"
DATA_SAVED_MESSAGE = "Tags have been modified successfully"
CANCELED_MESSAGE = "Tag modification has been canceled."


def _query_library(library: library, query: str) -> List[Item]:
    media_items = list(library.items(decargs(query)))

    if not media_items:
        raise UserError("No matching items found.")

    return media_items


def _modify_media_items(
    media_items: List[Item],
    tag_names: List[str],
    tag_modifications: Dict[str, str],
) -> int:
    total_modifications_counter = 0

    for media_item in media_items:
        for tag_name in tag_names:
            total_modifications_counter += modify_media_item_tag(
                media_item, tag_name, tag_modifications
            )

    return total_modifications_counter


def _save_media_items(media_items: List[Item]) -> None:
    for media_item in media_items:
        media_item.store()


def _ask_user_to_save_modifications(media_items: List[Item]) -> None:
    user_has_confirmed = ui.input_yn(CONFIRMATION_PROMPT, require=True)

    if user_has_confirmed:
        _save_media_items(media_items)
        ui.print_(DATA_SAVED_MESSAGE)

    else:
        ui.print_(CANCELED_MESSAGE)


def tagmod_command_function(
    library: library, options: optparse.Values, arguments: List[str]
) -> None:
    media_items = _query_library(library, options.media_query)
    tag_modifications = parse_arguments_as_tag_modifications(arguments)
    modification_counter = _modify_media_items(
        media_items, options.tag_names, tag_modifications
    )

    if modification_counter > 0:
        _ask_user_to_save_modifications(media_items)

    else:
        ui.print_("Nothing to do")
