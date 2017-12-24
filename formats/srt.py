from formats import formatter


def prefix() -> str:
    return ''


def suffix() -> str:
    return ''


def comment(comment: dict) -> str:
    lines: list = [
        '1'
    ]

    return value


def convert(comment: dict) -> str:
    return '{}{}{}'.format(prefix(), line(comment), suffix())
