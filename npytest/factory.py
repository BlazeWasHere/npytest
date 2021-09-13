#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
import random

from nertivia.cache_nertivia_data import LimitedCache
import nertivia

from .http import MockHTTPClient

# Our representation of nertivia.cache_nertivia_data.messages.
_messages = LimitedCache()
# Used internally to keep messages in sync within funcs.
_message_ids: List[int] = []


class MockMessage(nertivia.Message):
    async def send(self, message: str) -> nertivia.Message:
        mes = make_message(message)
        _messages[mes.id] = mes
        _message_ids.append(mes.id)

        return mes

    async def edit(self, content) -> None:
        _messages[self.id].content = content
        _message_ids.append(self.id)

    async def delete(self) -> None:
        del _messages[self.id]


class MockChannel(nertivia.Channel):
    async def send(self, message: str) -> nertivia.Message:
        mes = make_message(message)
        _messages[mes.id] = mes
        _message_ids.append(mes.id)

        return mes

    async def get_message(self, message_id: str) -> Optional[nertivia.Message]:
        return _messages.get(message_id)


def _random_id() -> int:
    return random.randrange(10000000000000000000)


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
            'messageID': _random_id()
        }
    }

    obj = MockMessage(data, http=MockHTTPClient())
    _messages[obj.id] = obj

    return obj


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
