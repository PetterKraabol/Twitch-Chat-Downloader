from formats import formatter


def ssa(comment: dict) -> str:
    return formatter.use('ssa', comment)


def prefix() -> str:
    return ''


def postfix() -> str:
    return ''
