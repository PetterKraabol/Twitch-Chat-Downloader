from formats import formatter


def srt(comment: dict) -> str:
    return formatter.use('srt', comment)


def prefix() -> str:
    return ''


def postfix() -> str:
    return ''
