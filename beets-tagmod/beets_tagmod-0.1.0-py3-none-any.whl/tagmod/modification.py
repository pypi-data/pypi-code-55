import re
from typing import Dict

from beets.library import Item

from beetsplug.tagmod.logging import LoggingWrapper


def _media_item_to_string(media_item: Item) -> str:
    artist = media_item.get("artist", "unknown artist")
    title = media_item.get("title", "unknown title")
    return f"<MediaItem '{artist}' - '{title}'>"


def _media_item_has_tag(media_item: Item, tag_name: str) -> bool:
    return tag_name in media_item


def _log_item_tag_changes(
    media_item: Item,
    tag_name: str,
    original_tag_value: str,
    new_tag_value: str,
    applied_modifications_counter: int,
) -> None:
    if applied_modifications_counter > 0:
        LoggingWrapper.get_instance().info(
            f"Changed tag '{tag_name}' of {_media_item_to_string(media_item)} "
            f" from '{original_tag_value}' to '{new_tag_value}' "
            f"({applied_modifications_counter} applied modifications)"
        )

    else:
        LoggingWrapper.get_instance().debug("Tag value remains unchanged")


def _replace_media_items_tag(
    media_item: Item, tag_name: str, pattern: str, replacement: str
) -> int:
    LoggingWrapper.get_instance().debug(
        f"Substitute '{pattern}' with '{replacement}'"
    )
    original_tag_value = media_item[tag_name]
    new_tag_value = re.sub(pattern, replacement, original_tag_value)

    if new_tag_value != original_tag_value:
        LoggingWrapper.get_instance().debug(
            f"Changed '{original_tag_value}' to '{new_tag_value}'"
        )
        media_item[tag_name] = new_tag_value
        return 1

    else:
        LoggingWrapper.get_instance().debug("Original value remains unchanged")
        return 0


def modify_media_item_tag(
    media_item: Item, tag_name: str, tag_modifications: Dict[str, str]
) -> int:
    LoggingWrapper.get_instance().debug(
        f"Modify tag '{tag_name}' with '{tag_modifications}'"
    )

    if not _media_item_has_tag(media_item, tag_name):
        LoggingWrapper.get_instance().warning(
            f"Media item has not such tag '{tag_name}'!"
        )
        return 0

    original_tag_value = media_item[tag_name]
    new_tag_value = original_tag_value
    applied_modifications_counter = 0

    for pattern, replacement in tag_modifications.items():
        modifications = _replace_media_items_tag(
            media_item, tag_name, pattern, replacement
        )
        applied_modifications_counter += modifications
        new_tag_value = media_item[tag_name]

    _log_item_tag_changes(
        media_item,
        tag_name,
        original_tag_value,
        new_tag_value,
        applied_modifications_counter,
    )

    return applied_modifications_counter


def modify_media_item(
    media_item: Item, modifications: Dict[str, Dict[str, str]]
) -> None:
    LoggingWrapper.get_instance().debug(
        f"Modify the tags of {_media_item_to_string(media_item)}"
    )
    for tag_name, tag_modifications in modifications.items():
        modify_media_item_tag(media_item, tag_name, tag_modifications)
