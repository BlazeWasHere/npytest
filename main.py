#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nertivia

from npytest.mock import configure
import npytest

client = nertivia.Bot()


@client.event
async def on_ready():
    print("Logged in as", client.user.username)


@client.event
async def on_quit():
    print("I'm disconnected!")


@client.event
async def on_status_change(data):
    print(data)


@client.event
async def on_message(message: nertivia.Message):
    if message.content.startswith("!ping"):
        await message.channel.send("pong")


if __name__ == '__main__':
    configure(client)

    assert not npytest.message('hello')
    assert npytest.message('!ping')[0].content == 'pong'
