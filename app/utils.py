import random


class SafeDict(dict):
    def __missing__(self, key):
        print(key)
        return '{' + key + '}'


def random_color() -> str:
    def r() -> int:
        return random.randint(0, 255)

    return '#%02X%02X%02X' % (r(), r(), r())
