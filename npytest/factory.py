#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

import nertivia

from .http import MockHTTPClient

_messages: List[nertivia.Message] = []


class MockMessage(nertivia.Message):
    async def send(self, message: str) -> None:
        mes = make_message(message)
        _messages.append(mes)


class MockChannel(nertivia.Channel):
    async def send(self, message: str) -> None:
        mes = make_message(message)
        _messages.append(mes)


def make_message(message: str) -> nertivia.Message:
    data = {
        'message': {
            'channelID': '0000000000000000000',
            'message': message,
            'creator': {
                'id': '0',
                'username': 'npytest',
                'tag': '0000',
                'avatar': None
            },
            'created': 0000000000000,
            'mentions': [],
            'quotes': [],
            'messageID': '0000000000000000000'
        }
    }

    return MockMessage(data, http=MockHTTPClient())


def make_channel(channel_id: int) -> nertivia.Channel:
    data = {
        'name': 'npytest',
        'channelID': channel_id,
        'server_id': '0000000000000000000'
    }

    return MockChannel(data, http=MockHTTPClient())


def make_server(server_id: int) -> nertivia.Server:
    data = {
        '_id': server_id,
        'avatar': None,
        'channel_position': [],
        'name': 'npytest',
        'creator': {
            'id': '0000000000000000000'
        },
        'default_channel_id': '0000000000000000000',
        'server_id': '0000000000000000000',
        'banner': None,
        'channels': []
    }

    obj = nertivia.Server(data)
    obj.http = MockHTTPClient()

    return obj


def make_user(user_id: int) -> nertivia.User:
    data = {
        "user": {
            "_id": "000000000000000000000000",
            "avatar": None,
            "username": "npytest",
            "tag": "1337",
            "created": 0000000000000,
            "about_me": {
                "_id": "000000000000000000000000",
                "gender": "foo",
                "age": "foo",
                "continent": "foo",
                "country": "foo",
                "about_me": "foo"
            },
            "id": user_id
        },
        "commonServersArr": [],
        "commonFriendsArr": [],
        "isBlocked": False
    }

    return nertivia.User(data)
