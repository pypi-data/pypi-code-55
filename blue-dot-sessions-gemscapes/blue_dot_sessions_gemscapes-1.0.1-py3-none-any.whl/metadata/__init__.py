import logging

import eyed3

module_logger = logging.getLogger(__name__)


def get_mp3_gemscape_characteristics(file_path: str) -> list:
    """
    Get Blue Dot Sessions characteristics from .mp3 file.
    """
    id_locator = "ID:"
    audiofile = eyed3.load(file_path)
    for comment in audiofile.tag.comments:
        if id_locator in comment.text:
            start_idx = comment.text.find(id_locator)
            end_idx = comment.text.find(".", start_idx)
            characteristics = comment.text[start_idx + len(id_locator):end_idx]
            return [int(val) for val in characteristics]
    return []
