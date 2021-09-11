#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nertivia


class MockHTTPClient(nertivia.HTTPClient):
    async def send_message(self, channel_id, content) -> None:
        # TODO: raise runtimeerror?
        pass

    def get_channel(self, channel_id: int):
        # Prevent circular import.
        from .factory import make_channel

        return make_channel(channel_id)

    def get_server(self, server_id, force_cache: bool = False):
        # Prevent circular import.
        from .factory import make_server

        if str(server_id) in nertivia.cache_nertivia_data.guilds:
            return nertivia.cache_nertivia_data.guilds[str(server_id)]
        elif not force_cache:
            return make_server(server_id)

        return None
