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
class InlineQueryResultVoice(InlineQueryResult):
    """\
    Represents InlineQueryResultVoice object:
    https://core.telegram.org/bots/api#inlinequeryresultvoice
    """

    type: str = field(init=False, default='voice')

    id: str
    voice_url: str
    title: str
    caption: Optional[str] = None
    parse_mode: Optional[ParseModeType] = None
    voice_duration: Optional[int] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
