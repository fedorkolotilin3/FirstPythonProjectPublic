from enum import Enum


class Keys(Enum):
    ESCAPE = 1
    DOWN = 2
    ACTIVATE = 3
    UP = 4
    RIGHT = 5
    LEFT = 6
    BACKSPACE = 7


key_codes = {"KEY_ESCAPE": [27, ""], "KEY_ACTIVATE": [410, '\n'], "KEY_UP": [259],
             "KEY_DOWN": [258], "KEY_RIGHT": [260], "KEY_LEFT": [261]}
key_codes_new = {Keys.ESCAPE: [27, ""], Keys.ACTIVATE: [410, '\n'], Keys.UP: [259],
                 Keys.DOWN: [258], Keys.RIGHT: [260], Keys.LEFT: [261], Keys.BACKSPACE: [263]}


def get_key(value):
    for key in key_codes_new:
        if value in key_codes_new[key]:
            return True, key
    return False, value
