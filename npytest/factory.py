#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
import nertivia

from .http import MockHTTPClient

_messages: List[nertivia.Message] = []


class MockMessage(nertivia.Message):
    def __init__(self, message, **kwargs):
        """
        Set different variables that'll be used later on for ease of access
        """
        # If a message object is passed then use its information to create this Message object
        # Otherwise create a new one from nothing
        # rewrite `nertivia.Channel` to use `MockHTTPClient`
        self.http = MockHTTPClient()

        if "message" in message:
            self.id: int = message['message']['messageID']
            self.content: str = message['message']['message']
            self.channel: nertivia.Channel = self.http.get_channel(
                message["message"]["channelID"])
            self.author: str = message['message']['creator'][
                'username'] + '@' + message['message']['creator']['tag']

        else:
            self.id: int = message['messageID']
            self.content: str = message['message']
            self.channel: nertivia.Channel = self.http.get_channel(
                message["channelID"])
            self.author: str = message['creator']['username'] + '@' + message[
                'creator']['tag']

        self.server: nertivia.Server = self.channel.server


class MockChannel(nertivia.Channel):
    def __init__(self, channel, **kwargs):
        # rewrite `nertivia.Channel` to use `MockHTTPClient`
        self.http = MockHTTPClient()

        # Set all of the properties of the channel in a self.x blob, consider cleaning up if possible
        # If a Channel object is provided in the arguments, then just extract all of its information
        if "channel" in channel:
            self.id = channel["channel"]["channelID"]
            self.name = channel["channel"]["name"]
            self.status = channel["channel"]["status"]
            self.name = channel["channel"]["name"]
            self.server = self.http.get_server(  # type: ignore
                channel["channel"]["server_id"])
            self.last_messaged = channel["channel"]["timestamp"]
            self._channel = channel["channel"]

        # If it is a new Channel object, then we have less information to set and use what was provided
        else:
            self.id = channel["channelID"]
            self.name = channel["name"]
            self.server = self.http.get_server(  # type: ignore
                channel["server_id"])
            if "timestamp" in channel:
                self.last_messaged = channel["timestamp"]
            self._channel = channel

    async def send(self, message: str):
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

    return MockMessage(data)


def make_channel(channel_id: int) -> nertivia.Channel:
    data = {
        'name': 'dpytest',
        'channelID': channel_id,
        'server_id': '0000000000000000000'
    }

    return MockChannel(data)


def make_server(server_id: int) -> nertivia.Server:
    data = {
        '_id': server_id,
        'avatar': None,
        'channel_position': [],
        'name': 'dpytest',
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
