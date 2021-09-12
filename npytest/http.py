#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings

import nertivia


class MockHTTPClient(nertivia.HTTPClient):
    def __runtime_warn(self, func: str) -> None:
        warnings.warn(f'{func} is not implemented in {self.__class__}',
                      RuntimeWarning)

    async def delete_message(self, message_id, channel_id) -> None:
        self.__runtime_warn('delete_message()')

    async def edit_message(self, message_id, channel_id, content: str) -> None:
        self.__runtime_warn('edit_message()')

    async def send_message(self, channel_id, content) -> None:
        self.__runtime_warn('send_message()')

    async def get_message(self, message_id, channel_id) -> None:
        self.__runtime_warn('get_message()')

    def get_channel(self, channel_id: int):
        # Prevent circular import.
        from .factory import make_channel

        return make_channel(channel_id)

    def get_user(self, user_id, force_cache: bool = False):
        # Prevent circular import.
        from .factory import make_user

        if str(user_id) in nertivia.cache_nertivia_data.users:
            return nertivia.cache_nertivia_data.users[str(user_id)]
        elif not force_cache:
            return make_user(user_id)

        return None

    def get_server(self, server_id, force_cache: bool = False):
        # Prevent circular import.
        from .factory import make_server

        if str(server_id) in nertivia.cache_nertivia_data.guilds:
            return nertivia.cache_nertivia_data.guilds[str(server_id)]
        elif not force_cache:
            return make_server(server_id)

        return None
