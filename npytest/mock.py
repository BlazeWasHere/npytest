#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
import asyncio

import nertivia

from .callbacks import set_callback, dispatch_event
from .factory import make_message, _messages
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
    # Clear `_messages` to remove any data from the last run.
    _messages.clear()

    if not asyncio.run(dispatch_event('receiveMessage', obj)):
        raise TypeError('receiveMessage callback has not been set')

    return _messages
