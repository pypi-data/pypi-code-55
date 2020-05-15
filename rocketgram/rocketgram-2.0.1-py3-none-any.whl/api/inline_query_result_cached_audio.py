# Copyright (C) 2015-2020 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


from dataclasses import dataclass, field
from typing import Optional

from .inline_keyboard_markup import InlineKeyboardMarkup
from .inline_query_result import InlineQueryResult
from .input_message_content import InputMessageContent
from .parse_mode_type import ParseModeType


@dataclass(frozen=True)
class InlineQueryResultCachedAudio(InlineQueryResult):
    """\
    Represents InlineQueryResultCachedAudio object:
    https://core.telegram.org/bots/api#inlinequeryresultcachedaudio
    """

    type: str = field(init=False, default='audio')

    id: str
    audio_file_id: str
    caption: Optional[str] = None
    parse_mode: Optional[ParseModeType] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
