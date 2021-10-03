#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nertivia
import pytest

import npytest


@pytest.fixture
def bot():
    client = nertivia.Bot()

    @client.event
    async def on_message(message: nertivia.Message):
        if message.content.startswith("!ping"):
            await message.channel.send("pong")

    npytest.configure(client)
    return client


def test_bot_instance(bot) -> None:
    assert isinstance(bot, nertivia.Bot)


def test_message_edit() -> None:
    mes = npytest.message('hello')[0]
    mes1 = npytest.edit(mes, 'bye')

    assert mes == mes1
    assert mes1.content == 'bye'
    assert mes.content == 'bye'


def test_message_ping() -> None:
    msgs = npytest.message('!ping')

    assert len(msgs) == 2
    assert msgs[1].content == 'pong'


def test_no_bot_message() -> None:
    assert len(npytest.message('foo')) == 1


def test_edit_not_found() -> None:
    mes = npytest.message('foo')[0]
    # Internal message cache key is by `id`, change it to invalidate the cache.
    mes.id = 1

    assert npytest.edit(mes, 'bar') is None
