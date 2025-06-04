import Engine.error

import Engine.objects
import Engine.assets

import Engine.window
import Engine.time

from Engine.app import App

_increment: int = -1


def get_identifier():
    global _increment
    _increment += 1
    return str(_increment)


def can_be_empty_content(value):
    if is_not_err(value) and value is not None:
        return value.content


def is_not_err(value):
    return not isinstance(value, Engine.error.Error)


def is_not_none(value):
    return value is not None
