#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
import asyncio

import nertivia

from .factory import make_message, _messages, _message_ids
from .callbacks import set_callback, dispatch_event
from .http import MockHTTPClient


def configure(bot: nertivia.Bot):
    if not isinstance(bot, nertivia.Bot):
        raise TypeError("bot must be an instance of nertivia.Bot")

    bot.http = MockHTTPClient()

    # `_` is should be '/' and value should be Dict[str, List[Callable]],
    # but better to be safe.
    for _, value in bot.sio.handlers.items():
        for event, array in value.items():
            # Only use the FIRST callback/function pointer
            set_callback(array[0], event)


def message(msg: str) -> List[nertivia.Message]:
    obj = make_message(msg)
    # Clear previous message states.
    _message_ids.clear()

    if not asyncio.run(dispatch_event('receiveMessage', obj)):
        raise TypeError('receiveMessage callback has not been set')

    ret = [obj]

    if _message_ids:
        # Make and fill an array with every message which has been added.
        ret += [_messages[i] for i in _message_ids]

    return ret


def edit(msg: nertivia.Message, content: str) -> nertivia.Message:
    # Clear previous message states.
    _message_ids.clear()

    asyncio.run(msg.edit(content))

    return msg
