#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Callable, Dict, Coroutine, Optional

Callback = Callable[..., Coroutine[None, None, None]]

_callbacks: Dict[str, Callback] = {}


async def dispatch_event(event: str, *args, **kwargs) -> bool:
    cb = _callbacks.get(event)

    if cb is not None:
        await cb(*args, **kwargs)
        return True

    return False


def set_callback(cb: Callback, event: str) -> None:
    _callbacks[event] = cb


def get_callback(event: str) -> Optional[Callback]:
    return _callbacks.get(event)


def remove_callback(event: str) -> Optional[Callback]:
    return _callbacks.pop(event, None)
