# Copyright (C) 2015-2020 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


from dataclasses import dataclass
from typing import Union

from .request import Request
from .. import api


@dataclass(frozen=True)
class GetChatMember(Request):
    """\
    Represents GetChatMember request object:
    https://core.telegram.org/bots/api#getchatmember
    """

    chat_id: Union[int, str]
    user_id: int

    def parse_result(self, data) -> 'api.ChatMember':
        assert isinstance(data, dict), "Should be dict."
        return api.ChatMember.parse(data)

    async def send2(self) -> 'api.ChatMember':
        res = await self._send()
        return res.result
