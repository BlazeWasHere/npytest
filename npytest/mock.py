#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
import asyncio

import nertivia

from .factory import make_message, _messages, _message_ids
from .callbacks import set_callback, dispatch_event
from .http import MockHTTPClient


def configure(bot: nertivia.Bot):
    """
    The "init" command of npytest. Call it to setup your nertivia bot.

    Args:
        bot (nertivia.Bot): Object of the nertivia.py bot.

    Raises:
        TypeError: If `bot` is not an instance of `nertivia.Bot`.
    """

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
    """
    Mock a message in a mock nertivia channel.

    Args:
        msg (str): The mock message content.

    Raises:
        TypeError: If there is no `on_message` callback set.

    Returns:
        List[nertivia.Message]: List of mock `nertivia.Message`s sent by the bot.
            The first message of the array is the message sent by this function.

    Examples:
        >>> message('test')
        [<id=9993649525527305728 content='test' channel=<<id=0000000000000000000 name='npytest' server=<<id=0000000000000000000 name='npytest' default_channel=<0000000000000000000>>>>> server=<<id=0000000000000000000 name='npytest' default_channel=<0000000000000000000>>> author='npytest@0000'>]
        >>> message('!ping')[0]
        <id=6986161856568744966 content='pong' channel=<<id=0000000000000000000 name='npytest' server=<<id=0000000000000000000 name='npytest' default_channel=<0000000000000000000>>>>> server=<<id=0000000000000000000 name='npytest' default_channel=<0000000000000000000>>> author='npytest@0000'>
    """

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
    """
    Edit a mock nertivia.Message and change it's content to `content`.

    Note:
        Internally, if `msg` does not exist, None is returned.

    Args:
        msg (nertivia.Message): The nertivia.Message object to change.
        content (str): The content to change `msg.content` to.

    Returns:
        nertivia.Message: Exact same as `msg`.
    """

    # Clear previous message states.
    _message_ids.clear()

    try:
        asyncio.run(msg.edit(content))
    except KeyError:
        # `msg` does not exist.
        return None

    return msg
