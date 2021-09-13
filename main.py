#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nertivia

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
    npytest.configure(client)

    assert len(npytest.message('hello')) == 1

    mes = npytest.message('hi')[0]
    assert mes.content == 'hi'
    assert npytest.edit(mes, 'bye').content == 'bye'

    assert npytest.message('!ping')[1].content == 'pong'
